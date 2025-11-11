import sqlite3
from crear_base import crear_tabla_vehiculos
def agregar_vehiculo():
    print("\n--- Ingreso de Nuevo Vehículo ---")
    try:
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        año = int(input("Año: "))
        tipo = input("Tipo: ")
        cantidad = int(input("Cantidad en Stock: "))
        uso = input("Uso: ")

        crear_tabla_vehiculos()
        con=sqlite3.connect("gestion_empresarial.db")
        cursor=con.cursor()
        cursor.execute("""
        INSERT INTO VEHICULOS (marca, modelo, año, tipo, cantidad, uso)
        VALUES (?, ?, ?, ?, ?, ?)""",(marca,modelo,año,tipo,cantidad,uso))
        con.commit()
        con.close()
        print("\nVehículo agregado exitosamente")
    except ValueError:
        print("\n🚫 Error: El Año y la Cantidad deben ser números enteros.")
    except Exception as e:
        print(f"\n🚫 Ocurrió un error inesperado: {e}")


def eliminar_vehiculo():
    eliminar_id = input("Ingresa el ID del vehículo que deseas eliminar: ").strip()

    # Validar que el ID sea un número
    if not eliminar_id.isdigit():
        print("❌ Error: El ID debe ser un número válido.")
        return

    con = sqlite3.connect("gestion_empresarial.db")
    cursor = con.cursor()

    # Verificar si el vehículo existe antes de eliminar
    cursor.execute("SELECT * FROM VEHICULOS WHERE id = ?", (eliminar_id,))
    vehiculo = cursor.fetchone()

    if vehiculo is None:
        print("⚠️ No existe ningún vehículo con ese ID.")
        con.close()
        return

    # Confirmar eliminación
    confirmar = input(f"¿Está seguro de eliminar el vehículo con ID {eliminar_id}? (s/n): ").lower().strip()
    if confirmar != "s":
        print("❎ Operación cancelada.")
        con.close()
        return

    # Eliminar vehículo
    cursor.execute("DELETE FROM VEHICULOS WHERE id = ?", (eliminar_id,))
    con.commit()
    con.close()

    print("✅ Vehículo eliminado del inventario exitosamente.")


def editar_vehiculo():
    conn = None
    try:
        print("\n--- Edición de Vehículo ---")
        vehiculo_id = int(input("Ingresa el ID del vehículo a editar: "))
        
        marca = input("Nueva Marca (deja vacío para no cambiar): ")
        modelo = input("Nuevo Modelo (deja vacío para no cambiar): ")
        año_str = input("Nuevo Año (deja vacío para no cambiar): ")
        tipo = input("Nuevo Tipo (deja vacío para no cambiar): ")
        cantidad_str = input("Nueva Cantidad (deja vacío para no cambiar): ")
        uso = input("Nuevo Uso (deja vacío para no cambiar): ")

        campos_a_actualizar = []
        valores = []

        if marca:
            campos_a_actualizar.append("marca = ?")
            valores.append(marca)
        if modelo:
            campos_a_actualizar.append("modelo = ?")
            valores.append(modelo)
        if año_str:
            campos_a_actualizar.append("año = ?")
            valores.append(int(año_str))
        if tipo:
            campos_a_actualizar.append("tipo = ?")
            valores.append(tipo)
        if cantidad_str:
            campos_a_actualizar.append("cantidad = ?")
            valores.append(int(cantidad_str))
        if uso:
            campos_a_actualizar.append("uso = ?")
            valores.append(uso)

        if not campos_a_actualizar:
            print("No se proporcionaron campos para actualizar. Operación cancelada.")
            return

        valores.append(vehiculo_id) 

        sql_update = f"""
        UPDATE VEHICULOS 
        SET {', '.join(campos_a_actualizar)}
        WHERE id = ?
        """
        
        conn = sqlite3.connect("gestion_empresarial.db")
        cursor = conn.cursor()
        
        cursor.execute(sql_update, tuple(valores))
        
        if cursor.rowcount == 0:
            print(f"No se encontró un vehículo con ID {vehiculo_id} para actualizar.")
        else:
            conn.commit()
            print(f"Vehículo con ID {vehiculo_id} actualizado exitosamente.")

    except ValueError:
        print("Error: El ID, el Año y la Cantidad deben ser números enteros.")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        if conn:
            conn.close()


def buscar_vehiculo():
    conn = None
    try:
        print("\n--- Búsqueda de Vehículo ---")
        criterio = input("Buscar por ID, Marca o Modelo (escribe el valor): ")
        
        conn = sqlite3.connect("gestion_empresarial.db")
        cursor = conn.cursor()

        try:
            vehiculo_id = int(criterio)
            sql_select = "SELECT * FROM VEHICULOS WHERE id = ?"
            cursor.execute(sql_select, (vehiculo_id,))
            
        except ValueError:
            sql_select = """
            SELECT * FROM VEHICULOS 
            WHERE marca LIKE ? OR modelo LIKE ?
            """
            # El uso de '%' permite encontrar coincidencias parciales
            busqueda = ('%' + criterio + '%', '%' + criterio + '%')
            cursor.execute(sql_select, busqueda)

        resultados = cursor.fetchall()

        if not resultados:
            print(f"❌ No se encontraron vehículos que coincidan con '{criterio}'.")
            return

        print("\n✅ Resultados de la Búsqueda:")
        print("-" * 60)
        # Mostrar encabezados
        print(f"{'ID':<4} {'Marca':<15} {'Modelo':<15} {'Año':<6} {'Cantidad':<10} {'Uso':<10}")
        print("-" * 60)
        
        for fila in resultados:
            id_val, marca, modelo, año, tipo, cantidad, uso = fila
            print(f"{id_val:<4} {marca:<15} {modelo:<15} {año:<6} {cantidad:<10} {uso:<10}")
            
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
        
    finally:
        if conn:
            conn.close()


def listar_vehiculos():
    conn = None
    try:
        print("\n--- Listado Completo de Vehículos ---")
        
        conn = sqlite3.connect("gestion_empresarial.db")
        cursor = conn.cursor()

        # Consulta SQL para seleccionar TODOS los vehículos
        sql_select = "SELECT * FROM VEHICULOS"
        cursor.execute(sql_select)

        resultados = cursor.fetchall()

        if not resultados:
            print("❌ El inventario de vehículos está vacío.")
            return

        print("\n✅ Inventario Actual:")
        print("-" * 60)
        # Mostrar encabezados
        print(f"{'ID':<4} {'Marca':<15} {'Modelo':<15} {'Año':<6} {'Cantidad':<10} {'Uso':<10}")
        print("-" * 60)
        
        # Iterar e imprimir los resultados
        for fila in resultados:
            id_val, marca, modelo, año, tipo, cantidad, uso = fila
            print(f"{id_val:<4} {marca:<15} {modelo:<15} {año:<6} {cantidad:<10} {uso:<10}")
            
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
        
    finally:
        if conn:
            conn.close()

