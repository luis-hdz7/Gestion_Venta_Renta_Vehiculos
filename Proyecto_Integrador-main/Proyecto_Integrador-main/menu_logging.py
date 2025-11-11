from loging import logging
from crear_cuenta import crear_cuenta

def menu_logging():
    print("¿Ya tienes una cuenta con nosotros?, inicia sesión o regístrate a continuación.")
    print("1. Iniciar sesión")
    print("2. Registrarse")

    while True:
        opcion = input("Elige una de las opciones:\n> ").strip()

        if opcion == "1":    
            return logging()  

        elif opcion == "2":
            nombre, apellido, email, contraseña = crear_cuenta()
            tipo_usuario = "cliente"
            cargo = None  # no aplica para clientes

            return nombre, apellido, email, contraseña, tipo_usuario, cargo

        else:
            print("❌ Opción no válida, intente con 1 o 2.\n")

