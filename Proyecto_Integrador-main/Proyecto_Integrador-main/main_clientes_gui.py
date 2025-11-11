import customtkinter as ctk
from tkinter import messagebox
import re

# Patrón de validación de tarjeta
patron = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')

# Catálogo de autos en venta
catalogo_venta = {
    "Audi R8": {"marca": "Audi", "modelo": "R8", "precio": 130000},
    "Toyota Supra": {"marca": "Toyota", "modelo": "Supra mk4", "precio": 112000},
    "Honda Civic": {"marca": "Honda", "modelo": "Civic", "precio": 14500},
    "Nissan GTR": {"marca": "Nissan", "modelo": "GTR", "precio": 70300},
    "Chevrolet Camaro": {"marca": "Chevrolet", "modelo": "Camaro ZL1", "precio": 75900},
    "Porsche 911": {"marca": "Porsche", "modelo": "911 Carrera", "precio": 61200}
}

# Catálogo de autos en renta
catalogo_renta = {
    "Nissan Frontier": {"marca": "Nissan", "modelo": "Frontier", "precio": 57.00},
    "Mazda CX-5": {"marca": "Mazda", "modelo": "CX-5", "precio": 42.00},
    "Geely COOLRAY": {"marca": "Geely", "modelo": "COOLRAY", "precio": 52.00},
    "Ford Focus": {"marca": "Ford", "modelo": "Focus", "precio": 38.00},
    "MINI Cooper": {"marca": "MINI", "modelo": "Cooper S", "precio": 27.00},
    "BMW X1": {"marca": "BMW", "modelo": "X1", "precio": 95.00},
    "Toyota Raize": {"marca": "Toyota", "modelo": "Raize", "precio": 40.00}
}


class ClientesApp(ctk.CTkToplevel):
    def __init__(self, master, nombre):
        super().__init__(master)
        self.master = master
        self.nombre = nombre

        self.title("Catálogo - León Motors")
        self.geometry("700x550")

        ctk.CTkLabel(self, text=f"🚘 Bienvenido {nombre} al Catálogo de León Motors",
                     font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(self, text="Ver autos en venta", command=self.mostrar_venta, width=200).pack(pady=10)
        ctk.CTkButton(self, text="Ver autos en renta", command=self.mostrar_renta, width=200).pack(pady=10)
        ctk.CTkButton(self, text="Cerrar sesión", command=self.cerrar_sesion, fg_color="red").pack(pady=20)

        self.textbox = ctk.CTkTextbox(self, width=600, height=250)
        self.textbox.pack(pady=10)

        self.transient(master)
        self.grab_set()

    # ------------------- CATÁLOGOS -------------------
    def mostrar_venta(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "🏷️ Autos disponibles para *compra*:\n\n")
        for nombre, datos in catalogo_venta.items():
            self.textbox.insert("end", f"{nombre} - {datos['marca']} {datos['modelo']} - ${datos['precio']}\n")
        self.elegir_auto("venta")

    def mostrar_renta(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "🚗 Autos disponibles para *renta*:\n\n")
        for nombre, datos in catalogo_renta.items():
            self.textbox.insert("end", f"{nombre} - {datos['marca']} {datos['modelo']} - ${datos['precio']} por día\n")
        self.elegir_auto("renta")

    # ------------------- TRANSACCIÓN -------------------
    def elegir_auto(self, tipo):
        win = ctk.CTkToplevel(self)
        win.title("Elegir vehículo")
        win.geometry("400x350")

        ctk.CTkLabel(win, text=f"Seleccione un vehículo para {tipo}", font=("Arial", 15, "bold")).pack(pady=10)

        catalogo = catalogo_venta if tipo == "venta" else catalogo_renta
        opciones = list(catalogo.keys())

        auto_opcion = ctk.CTkOptionMenu(win, values=opciones)
        auto_opcion.pack(pady=10)

        # Si es renta, pide cantidad de días
        dias_entry = None
        if tipo == "renta":
            ctk.CTkLabel(win, text="Cantidad de días (máx. 10):").pack(pady=5)
            dias_entry = ctk.CTkEntry(win, placeholder_text="Ejemplo: 3")
            dias_entry.pack(pady=5)

        def continuar():
            dias = 1
            if tipo == "renta":
                valor = dias_entry.get().strip()
                if not valor.isdigit():
                    messagebox.showerror("Error", "Ingrese un número válido de días.")
                    return
                dias = int(valor)
                if dias < 1 or dias > 10:
                    messagebox.showerror("Error", "El máximo permitido es 10 días.")
                    return
            self.procesar_pago(win, tipo, auto_opcion.get(), dias)

        ctk.CTkButton(win, text="Proceder con pago", command=continuar).pack(pady=15)

    def procesar_pago(self, ventana, tipo, auto, dias=1):
        ventana.destroy()

        datos = catalogo_venta[auto] if tipo == "venta" else catalogo_renta[auto]
        precio_total = datos['precio'] * dias if tipo == "renta" else datos['precio']

        win = ctk.CTkToplevel(self)
        win.title("Método de pago")
        win.geometry("400x420")

        ctk.CTkLabel(win, text=f"🚘 {auto}", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(win, text=f"Total a pagar: ${precio_total:.2f}", font=("Arial", 14)).pack(pady=5)
        if tipo == "renta":
            ctk.CTkLabel(win, text=f"{dias} día(s) de renta", font=("Arial", 13, "italic")).pack()

        ctk.CTkLabel(win, text="Seleccione método de pago:").pack(pady=10)

        metodo = ctk.StringVar(value="efectivo")
        ctk.CTkRadioButton(win, text="💵 Efectivo", variable=metodo, value="efectivo").pack()
        ctk.CTkRadioButton(win, text="💳 Tarjeta", variable=metodo, value="tarjeta").pack()

        frame_pago = ctk.CTkFrame(win)
        frame_pago.pack(pady=20)

        monto_entry = ctk.CTkEntry(frame_pago, placeholder_text="Monto entregado")
        tarjeta_entry = ctk.CTkEntry(frame_pago, placeholder_text="Número de tarjeta (####-####-####-####)")
        cvv_entry = ctk.CTkEntry(frame_pago, placeholder_text="CVV", show="*")

        def actualizar_campos(*args):
            for widget in frame_pago.winfo_children():
                widget.pack_forget()
            if metodo.get() == "efectivo":
                monto_entry.pack(pady=5)
            else:
                tarjeta_entry.pack(pady=5)
                cvv_entry.pack(pady=5)

        metodo.trace("w", actualizar_campos)
        actualizar_campos()

        def confirmar_pago():
            if metodo.get() == "efectivo":
                monto = monto_entry.get().strip()
                if not monto or not monto.replace(".", "").isdigit():
                    messagebox.showerror("Error", "Ingrese un monto válido.")
                    return
                messagebox.showinfo(
                    "Transacción exitosa",
                    f"✅ Pago en efectivo por ${monto} recibido.\nGracias por su {'renta' if tipo == 'renta' else 'compra'}, {self.nombre}!"
                )
            else:
                tarjeta = tarjeta_entry.get().strip()
                cvv = cvv_entry.get().strip()
                if not patron.match(tarjeta):
                    messagebox.showerror("Error", "Número de tarjeta inválido.")
                    return
                if len(cvv) != 3 or not cvv.isdigit():
                    messagebox.showerror("Error", "CVV inválido.")
                    return
                messagebox.showinfo(
                    "Transacción exitosa",
                    f"✅ Pago con tarjeta terminado.\nGracias por su {'renta' if tipo == 'renta' else 'compra'}, {self.nombre}!"
                )

            win.destroy()

        ctk.CTkButton(win, text="Confirmar pago", command=confirmar_pago).pack(pady=15)

    def cerrar_sesion(self):
        confirmar = messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?")
        if confirmar:
            self.destroy()
            self.master.deiconify()
