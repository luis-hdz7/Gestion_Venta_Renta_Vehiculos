import re
import sqlite3

def logging():
    logger = """
    __________________________________________
   |              INICIAR SESIÓN              |
    ------------------------------------------
    """
    print(logger)

    while True:
        errores = []

        email = input("Email:\n> ").strip()
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, email):
            errores.append("Email no válido, no cumple con el formato válido.")

        password = input("Password:\n> ").strip()
        if len(password) > 15 or len(password) < 8:
            errores.append("La contraseña debe tener entre 8 y 15 caracteres.")

        if errores:
            print("\n❌ Errores encontrados:")
            for error in errores:
                print(f"- {error}")
            print("Corrija los errores e intente nuevamente.\n")
            continue

        #*Se verifica si el usuario es trabajador
        conn = sqlite3.connect("registro_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, correo, contrasena, cargo FROM empleados WHERE correo = ?", (email,))
        empleado = cursor.fetchone()

        if empleado:
            nombre, apellido, correo, contrasena, cargo = empleado
            if password == contrasena:
                print(f"\n✅ Inicio de sesión exitoso. Bienvenido {nombre} ({cargo}).\n")
                tipo_usuario = "empleado"
                conn.close()
                return nombre, apellido, correo, password, tipo_usuario, cargo
            else:
                print("❌ Contraseña incorrecta.\n")
                conn.close()
                continue

        #*Si no es empleado se busca en usuarios normales
        cursor.execute("SELECT nombre, apellido, email, contraseña FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario is None:
            print("⚠️ No existe ninguna cuenta registrada con ese email.\n")
            continue
        elif usuario[3] != password:
            print("❌ Contraseña incorrecta.\n")
            continue
        else:
            nombre, apellido, email, contraseña = usuario
            print(f"\n✅ Inicio de sesión exitoso. ¡Bienvenido {nombre}!\n")
            tipo_usuario = "cliente"
            cargo = None  #No aplica para clientes
            return nombre, apellido, email, contraseña, tipo_usuario, cargo