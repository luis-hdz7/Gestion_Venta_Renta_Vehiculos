import customtkinter as ctk
from tkinter import messagebox
import re
from base_datos import crear_tablas
import sqlite3

class RegistroApp(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Crear cuenta")
        self.geometry("400x450")
        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self, text="CREAR CUENTA", font=("Arial", 20, "bold")).pack(pady=20)
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=5)
        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        self.entry_apellido.pack(pady=5)
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Correo electrónico")
        self.entry_email.pack(pady=5)
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_password.pack(pady=5)

        ctk.CTkButton(self, text="Registrar", command=self.registrar_usuario).pack(pady=20)
        ctk.CTkButton(self, text="Volver al menú principal", fg_color="gray", command=self.volver_menu).pack(pady=5)

        # Hace que esta ventana bloquee la principal (modal)
        self.transient(master)
        self.grab_set()

    def registrar_usuario(self):
        import re, sqlite3
        from base_datos import crear_tablas

        nombre = self.entry_nombre.get().strip().capitalize()
        apellido = self.entry_apellido.get().strip().capitalize()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        errores = []
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not nombre.isalpha():
            errores.append("El nombre solo puede contener letras.")
        if not apellido.isalpha():
            errores.append("El apellido solo puede contener letras.")
        if not re.match(patron_email, email):
            errores.append("Formato de email no válido.")
        if len(password) < 8 or len(password) > 15:
            errores.append("La contraseña debe tener entre 8 y 15 caracteres.")

        if errores:
            messagebox.showerror("Errores", "\n".join(errores))
            return

        crear_tablas()
        conn = sqlite3.connect("registro_users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, email, contraseña) VALUES (?, ?, ?, ?)",
                (nombre, apellido, email, password)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
            self.volver_menu()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Advertencia", "Ese email ya está registrado.")
        finally:
            conn.close()

    def volver_menu(self):
        self.destroy()
        self.master.deiconify()
