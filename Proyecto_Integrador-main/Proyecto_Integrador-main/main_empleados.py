import os
import time
import sys
import funciones_administativas
import funciones_gestion_autos as funcions



def mostrar_menu_empleados(nombre, cargo):
    while True:

        print(f"""
    __________________________________________
   |     SISTEMA DE GESTIÓN - EMPLEADOS       |
    ------------------------------------------
      👔 Bienvenido, {nombre} ({cargo})
    ------------------------------------------
      1. Ver Inventario de Autos
      2. Agregar al Catálogo
      3. Eliminar Auto del Inventario
      4. Editar Datos de un Auto
      5. Buscar un Auto en el Inventario
      6. Funciones administrativas
      7. Cerrar sesión
    __________________________________________
        """)

        opcion = input("Seleccione una opción\n> ").strip()

        if opcion == "1":
            print("🚗 Mostrando catálogo de vehículos...\n")
            funcions.listar_vehiculos()

        elif opcion == "2":
            funcions.agregar_vehiculo()

        elif opcion == "3":
            funcions.eliminar_vehiculo()


        elif opcion == "4":
            funcions.editar_vehiculo()


        elif opcion == "5":
            funcions.buscar_vehiculo()


        elif opcion == "6":
            print("\n🔐 Acceso restringido a funciones administrativas.")
            print("Solo los empleados con cargo 'Administrador' pueden continuar.\n")

            #*Verificar el cargo del usuario
            if cargo.lower() != "administrador":
                print("🚫 Acceso denegado. Tu cargo no permite ejecutar estas funciones.\n")
                input("Seleccione enter para regresar")
                continue

            #*Validar también la clave
            clave_correcta = "clave_admin456"
            intentos = 3

            while intentos > 0:
                clave_ingresada = input("Ingrese la clave de administrador:\n> ").strip()
                if clave_ingresada == clave_correcta:
                    print("\n✅ Acceso concedido. Bienvenido al panel administrativo.\n")
                    funciones_administativas.main()
                    return
                else:
                    intentos -= 1
                    print(f"❌ Clave incorrecta. Le quedan {intentos} intentos.\n")

            if intentos == 0:
                print("🚨 ¡Ha superado el límite de intentos! Cerrando acceso.\n")

        elif opcion == "7":
            print("\n👋 Cerrando sesión...")
            sys.exit()

        else:
            print("⚠️ Opción no válida, intente de nuevo.\n")

