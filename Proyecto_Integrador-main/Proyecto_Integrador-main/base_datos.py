import sqlite3

def crear_tablas():
    conn = sqlite3.connect("registro_users.db")
    cursor = conn.cursor()

    # 🧍 Tabla de usuarios (clientes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        contraseña TEXT NOT NULL
    )
    """)

    # 👔 Tabla de empleados (personal de la concesionaria)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        cargo TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    #print("✅ Tablas 'usuarios' y 'empleados' creadas o ya existentes.")
    conn = sqlite3.connect("registro_users.db")
    cursor = conn.cursor()



if __name__ == "__main__":
    crear_tablas()
