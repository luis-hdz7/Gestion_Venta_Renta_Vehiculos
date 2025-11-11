from helpers import capitalizar
import re
import sqlite3
import sys
def funciones_jefes():
    print(f"""
    _______________________________________________
   |        SISTEMA DE GESTIÓN - ADMINISTACION     |
    -----------------------------------------------
      👔 Bienvenido
    ------------------------------------------
      1. Ver personal de plantilla
      2. Registrar empleado
      3. Eliminar empleado
      4. Cerrar sesión
    __________________________________________
        """)
    opcion = input("Seleccione una opción: ").strip()
    return opcion

def registrar_empleado():
    print("Por favor, ingrese los datos para continuar.\n")

    while True:
        errores = []

        nombre = input("Nombre: ").strip()
        nombre = capitalizar(nombre)
        if not nombre.isalpha():
            errores.append("Nombre no válido, solo se admiten caracteres alfabéticos.")

        apellido = input("Apellido: ").strip()
        apellido = capitalizar(apellido)
        if not apellido.isalpha():
            errores.append("Apellido no válido, solo se admiten caracteres alfabéticos.")

        email = input("Correo corporativo (debe terminar en @leonmotors.com): ").strip()
        patron_email = r'^[\w\.-]+@leonmotors\.com$'
        if not re.match(patron_email, email):
            errores.append("Correo no válido. Debe usar un correo corporativo (@leonmotors.com).")

        password = input("Contraseña de autorización (solo para registrar empleados): ").strip()
        if password != "clave_admin123":
            errores.append("Contraseña de autorización incorrecta.")

        if errores:
            print("\n❌ Errores encontrados:")
            for error in errores:
                print(f"- {error}")
            print("Corrija los errores e intente nuevamente.\n")
            continue

        #*Definie el puesto y tipo de cargo
        puesto = input("Ingrese el puesto del empleado (ej. Ventas, Contador, Gerente): ").capitalize().strip()
        cargo = "Empleado"

        #Guardar en la base de datos
        conn = sqlite3.connect('registro_users.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO empleados (nombre, apellido, cargo, puesto, correo, contrasena)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, apellido, cargo, puesto, email, password))

            conn.commit()
            conn.close()
            print(f"\n✅ Empleado '{nombre} {apellido}' registrado exitosamente como {puesto}.\n")
            return nombre, apellido, email, password, cargo, puesto

        except sqlite3.IntegrityError:
            print("⚠️ El correo ya está registrado. Intente con otro correo.\n")
            conn.close()
            continue

def ver_empleados():
    conn = sqlite3.connect("registro_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, apellido, cargo, puesto, correo FROM empleados")
    empleados = cursor.fetchall()
    conn.close()

    if not empleados:
        print("\n⚠️ No hay empleados registrados.\n")
        return

    print("\n📋 LISTA DE EMPLEADOS REGISTRADOS\n")
    print("{:<5} {:<15} {:<15} {:<15} {:<15} {:<25}".format(
        "ID", "Nombre", "Apellido", "Cargo", "Puesto", "Correo"))
    print("-" * 90)

    for emp in empleados:
        id_, nombre, apellido, cargo, puesto, correo = emp
        print("{:<5} {:<15} {:<15} {:<15} {:<15} {:<25}".format(
            id_, nombre, apellido, cargo, puesto, correo))

    print("\n✅ Total de empleados registrados:", len(empleados))



def eliminar_empleado():
    print("\n🗑️  ELIMINAR EMPLEADO\n")

    conn = sqlite3.connect("registro_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, apellido, cargo, correo FROM empleados")
    empleados = cursor.fetchall()

    if not empleados:
        print("⚠️ No hay empleados registrados.\n")
        conn.close()
        return

    print("{:<5} {:<15} {:<15} {:<15} {:<25}".format("ID", "Nombre", "Apellido", "Cargo", "Correo"))
    print("-" * 75)

    for emp in empleados:
        print("{:<5} {:<15} {:<15} {:<15} {:<25}".format(*emp))

    try:
        id_empleado = int(input("\nIngrese el ID del empleado que desea eliminar: ").strip())
    except ValueError:
        print("❌ Debe ingresar un número válido.\n")
        conn.close()
        return

    cursor.execute("SELECT * FROM empleados WHERE id = ?", (id_empleado,))
    empleado = cursor.fetchone()

    if not empleado:
        print("⚠️ No existe ningún empleado con ese ID.\n")
        conn.close()
        return

    confirmar = input(f"¿Está seguro de eliminar al empleado '{empleado[1]} {empleado[2]}'? (s/n): ").strip().lower()
    if confirmar != "s":
        print("❎ Operación cancelada.\n")
        conn.close()
        return

    #!Eliminar empleado
    cursor.execute("DELETE FROM empleados WHERE id = ?", (id_empleado,))
    conn.commit()
    conn.close()

    print(f"✅ Empleado '{empleado[1]} {empleado[2]}' eliminado correctamente.\n")


def main():

        while True:
            opcion=funciones_jefes()
            match opcion:
                case "1":
                    ver_empleados()
                case "2":
                    registrar_empleado()
                case "3":
                    eliminar_empleado()
                case "4":
                    print("\nGracias por usar nuestro sistema...")
                    sys.exit()
                case _:
                    print("Caracter no reconocido, intetelo otra vez")

if __name__=="__main__":
    main()