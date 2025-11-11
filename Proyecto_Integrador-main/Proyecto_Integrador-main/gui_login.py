import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import re

class LoginApp(ctk.CTkToplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        self.title("Iniciar sesión")
        self.geometry("420x300")
        self.resizable(False, False)

        # Widgets
        ctk.CTkLabel(self, text="Iniciar sesión", font=("Arial", 20, "bold")).pack(pady=(20,10))
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Correo electrónico", width=320)
        self.entry_email.pack(pady=8)
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=320)
        self.entry_password.pack(pady=8)

        ctk.CTkButton(self, text="Ingresar", width=160, command=self.validar_login).pack(pady=(12,6))
        ctk.CTkButton(self, text="Cancelar", width=160, fg_color="gray", command=self.cancel).pack()

        # cuando el toplevel se cierra con la X, que vuelva a mostrar main
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        # Mostrar (no bloquear el mainloop del parent)
        self.transient(parent)
        self.grab_set()

    def validar_login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, email):
            messagebox.showerror("Error", "Formato de email inválido.")
            return
        if not (8 <= len(password) <= 15):
            messagebox.showerror("Error", "La contraseña debe tener entre 8 y 15 caracteres.")
            return

        # Verificar en la base de datos (empleados primero, luego usuarios)
        conn = sqlite3.connect("registro_users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, apellido, correo, contrasena, cargo FROM empleados WHERE correo = ?", (email,))
        empleado = cursor.fetchone()
        if empleado:
            nombre, apellido, correo, contrasena, cargo = empleado
            if password == contrasena:
                conn.close()
                # Llamar callback con nombre y cargo
                self.destroy()
                self.on_success(nombre, cargo)
                return
            else:
                conn.close()
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return

        # Si no es empleado, buscar en usuarios
        cursor.execute("SELECT nombre, apellido, email, contraseña FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario and usuario[3] == password:
            nombre, apellido, email, _ = usuario
            self.destroy()
            # Para clientes cargo = None o "cliente"
            self.on_success(nombre, "cliente")
            return

        messagebox.showerror("Error", "Credenciales inválidas o usuario no encontrado.")

    def cancel(self):
        # cerrar la ventana y devolver el foco al main
        self.destroy()
        self.parent.deiconify()