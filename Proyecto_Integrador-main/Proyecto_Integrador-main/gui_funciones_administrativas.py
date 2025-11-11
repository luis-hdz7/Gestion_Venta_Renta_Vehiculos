import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from helpers import capitalizar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DB_NAME = "registro_users.db"


class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panel Administrativo - León Motors")
        self.geometry("600x400")

        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="👔 Panel de Administración", font=("Arial", 20, "bold"))
        self.label.pack(pady=15)

        # Botones principales
        ctk.CTkButton(self.frame, text="📋 Ver empleados", command=self.ver_empleados).pack(pady=10)
        ctk.CTkButton(self.frame, text="➕ Registrar empleado", command=self.registrar_empleado).pack(pady=10)
        ctk.CTkButton(self.frame, text="🗑️ Eliminar empleado", command=self.eliminar_empleado).pack(pady=10)
        ctk.CTkButton(self.frame, text="🚪 Cerrar sesión", command=self.destroy).pack(pady=20)

    # ------------------- FUNCIONES -------------------
    def registrar_empleado(self):
        win = ctk.CTkToplevel(self)
        win.title("Registrar Empleado")
        win.geometry("400x450")

        ctk.CTkLabel(win, text="Registrar nuevo empleado", font=("Arial", 16, "bold")).pack(pady=10)

        nombre_entry = ctk.CTkEntry(win, placeholder_text="Nombre")
        apellido_entry = ctk.CTkEntry(win, placeholder_text="Apellido")
        correo_entry = ctk.CTkEntry(win, placeholder_text="Correo corporativo (@leonmotors.com)")
        puesto_entry = ctk.CTkEntry(win, placeholder_text="Puesto (Ventas, Contador, etc.)")
        clave_entry = ctk.CTkEntry(win, placeholder_text="Contraseña de autorización", show="*")

        for e in [nombre_entry, apellido_entry, correo_entry, puesto_entry, clave_entry]:
            e.pack(pady=5)

        def guardar_empleado():
            nombre = capitalizar(nombre_entry.get().strip())
            apellido = capitalizar(apellido_entry.get().strip())
            correo = correo_entry.get().strip()
            puesto = puesto_entry.get().strip().capitalize()
            clave = clave_entry.get().strip()

            errores = []
            if not nombre.isalpha() or not apellido.isalpha():
                errores.append("El nombre y apellido deben contener solo letras.")
            if not correo.endswith("@leonmotors.com"):
                errores.append("El correo debe ser corporativo (@leonmotors.com).")
            if clave != "clave_admin123":
                errores.append("Contraseña de autorización incorrecta.")

            if errores:
                messagebox.showerror("Errores", "\n".join(errores))
                return

            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO empleados (nombre, apellido, cargo, puesto, correo, contrasena)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nombre, apellido, "Empleado", puesto, correo, clave))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", f"Empleado {nombre} {apellido} agregado correctamente.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El correo ya está registrado.")

        ctk.CTkButton(win, text="Guardar empleado", command=guardar_empleado).pack(pady=20)

    def ver_empleados(self):
        win = ctk.CTkToplevel(self)
        win.title("Lista de Empleados")
        win.geometry("700x400")

        text = ctk.CTkTextbox(win, width=650, height=300)
        text.pack(padx=10, pady=10)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, cargo, puesto, correo FROM empleados")
        empleados = cursor.fetchall()
        conn.close()

        if not empleados:
            text.insert("0.0", "⚠️ No hay empleados registrados.")
            return

        encabezado = "{:<5} {:<15} {:<15} {:<15} {:<15} {:<25}\n".format(
            "ID", "Nombre", "Apellido", "Cargo", "Puesto", "Correo")
        text.insert("0.0", encabezado + "-" * 90 + "\n")

        for emp in empleados:
            linea = "{:<5} {:<15} {:<15} {:<15} {:<15} {:<25}\n".format(*emp)
            text.insert("end", linea)

    def eliminar_empleado(self):
        win = ctk.CTkToplevel(self)
        win.title("Eliminar Empleado")
        win.geometry("400x350")

        ctk.CTkLabel(win, text="Eliminar empleado por ID", font=("Arial", 15, "bold")).pack(pady=10)
        id_entry = ctk.CTkEntry(win, placeholder_text="Ingrese ID del empleado")
        id_entry.pack(pady=10)

        def eliminar():
            try:
                id_emp = int(id_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, apellido FROM empleados WHERE id = ?", (id_emp,))
            empleado = cursor.fetchone()

            if not empleado:
                messagebox.showwarning("No encontrado", "No existe un empleado con ese ID.")
                conn.close()
                return

            confirmar = messagebox.askyesno(
                "Confirmar", f"¿Eliminar a {empleado[0]} {empleado[1]}?"
            )
            if confirmar:
                cursor.execute("DELETE FROM empleados WHERE id = ?", (id_emp,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                win.destroy()
            else:
                conn.close()

        ctk.CTkButton(win, text="Eliminar empleado", fg_color="red", command=eliminar).pack(pady=20)


if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
