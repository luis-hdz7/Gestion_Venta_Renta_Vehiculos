import customtkinter as ctk
from gui_login import LoginApp
from gui_registro import RegistroApp
from main_empleados_gui import EmpleadosApp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚗 Concesionario León Motors")
        self.geometry("500x400")

        self.label_titulo = ctk.CTkLabel(self, text="🚗 Concesionario León Motors", font=("Arial", 22, "bold"))
        self.label_titulo.pack(pady=40)

        self.btn_login = ctk.CTkButton(self, text="Iniciar sesión", command=self.abrir_login)
        self.btn_login.pack(pady=10)

        self.btn_registro = ctk.CTkButton(self, text="Crear cuenta", command=self.abrir_registro)
        self.btn_registro.pack(pady=10)

        self.btn_salir = ctk.CTkButton(self, text="Salir", fg_color="red", hover_color="#b30000", command=self.destroy)
        self.btn_salir.pack(pady=10)

    def abrir_login(self):
        # Oculta el menú principal temporalmente
        self.withdraw()
        LoginApp(self, self.on_login_success)

    def abrir_registro(self):
        self.withdraw()
        RegistroApp(self)

    def on_login_success(self, nombre, cargo):
        """Callback cuando el login es exitoso"""
        # Ocultamos el menú principal (ya lo está, pero por seguridad)
        self.withdraw()

        if cargo and cargo.lower() in ["empleado", "administrador"]:
            print(f"✅ Login correcto como empleado: {nombre} ({cargo})")
            app = EmpleadosApp(self, nombre, cargo)
            app.focus_force()
        else:
            print(f"✅ Login correcto como cliente: {nombre}")
            from main_clientes_gui import ClientesApp
            app = ClientesApp(self, nombre)
            app.focus_force()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
