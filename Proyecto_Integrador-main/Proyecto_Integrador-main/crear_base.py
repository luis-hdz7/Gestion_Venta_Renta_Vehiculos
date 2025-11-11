import sqlite3

def crear_tabla_vehiculos():

    try:
        conn = sqlite3.connect("gestion_empresarial.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS VEHICULOS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            año INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            uso TEXT NOT NULL
        );
        """)

        conn.commit()
        #print("Tabla 'VEHICULOS' creada exitosamente o ya existía.")

    except sqlite3.Error as e:
        print(f"Ocurrió un error de SQLite: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    crear_tabla_vehiculos()