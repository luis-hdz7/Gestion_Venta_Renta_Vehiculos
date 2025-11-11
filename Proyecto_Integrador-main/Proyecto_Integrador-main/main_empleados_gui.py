import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import funciones_gestion_autos as funcions
from gui_funciones_administrativas import AdminApp


class EmpleadosApp(ctk.CTkToplevel):
    def __init__(self, parent, nombre, cargo):
        super().__init__(parent)
        self.title("Panel de Empleados - León Motors")
        self.geometry("600x550")
        self.resizable(False, False)

        self.nombre = nombre
        self.cargo = cargo
        self.parent = parent

        titulo = ctk.CTkLabel(
            self,
            text="🚗 SISTEMA DE GESTIÓN - EMPLEADOS 🚗",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=20)

        bienvenida = ctk.CTkLabel(
            self,
            text=f"👔 Bienvenido, {nombre} ({cargo})",
            font=("Arial", 14)
        )
        bienvenida.pack(pady=10)

        botones = [
            ("Ver Inventario de Autos", self.ver_inventario),
            ("Agregar al Catálogo", self.agregar_auto),
            ("Eliminar Auto del Inventario", self.eliminar_auto),
            ("Editar Datos de un Auto", self.editar_auto),
            ("Buscar un Auto", self.buscar_auto),
            ("Funciones Administrativas", self.funciones_admin),
            ("Cerrar Sesión", self.cerrar_sesion)
        ]

        for texto, comando in botones:
            btn = ctk.CTkButton(self, text=texto, command=comando, width=300, height=40, font=("Arial", 13))
            btn.pack(pady=8)

    # =====================================================
    # VENTANA DE INVENTARIO (tabla visual)
    # =====================================================
    def ver_inventario(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Inventario de Vehículos")
        ventana.geometry("850x500")

        # Conectar a la base de datos
        try:
            con = sqlite3.connect("gestion_empresarial.db")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM VEHICULOS")
            datos = cursor.fetchall()
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo acceder a la base de datos:\n{e}")
            return

        # Crear frame contenedor
        frame_tabla = ctk.CTkFrame(ventana)
        frame_tabla.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar
        tree_scroll = ttk.Scrollbar(frame_tabla)
        tree_scroll.pack(side="right", fill="y")

        # Crear la tabla (Treeview)
        columnas = ("ID", "Marca", "Modelo", "Año", "Tipo", "Cantidad", "Uso")
        tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=tree_scroll.set,
            height=18
        )
        tabla.pack(fill="both", expand=True)
        tree_scroll.config(command=tabla.yview)

        # Encabezados
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=110)

        # Insertar datos
        for fila in datos:
            tabla.insert("", "end", values=fila)

        # Si no hay registros
        if not datos:
            messagebox.showinfo("Inventario vacío", "No hay vehículos registrados actualmente.")

    # =====================================================
    # AGREGAR VEHÍCULO
    # =====================================================
    def agregar_auto(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Vehículo")
        ventana.geometry("400x500")

        campos = ["Marca", "Modelo", "Año", "Tipo", "Cantidad", "Uso"]
        entradas = {}

        for campo in campos:
            label = ctk.CTkLabel(ventana, text=campo)
            label.pack()
            entrada = ctk.CTkEntry(ventana, width=250)
            entrada.pack(pady=5)
            entradas[campo.lower()] = entrada

        def guardar():
            try:
                datos = {c: e.get() for c, e in entradas.items()}
                if not all(datos.values()):
                    messagebox.showwarning("Error", "❌ Debes llenar todos los campos.")
                    return
                # Convertir tipos
                datos["año"] = int(datos["año"])
                datos["cantidad"] = int(datos["cantidad"])

                con = sqlite3.connect("gestion_empresarial.db")
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO VEHICULOS (marca, modelo, año, tipo, cantidad, uso)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, tuple(datos.values()))
                con.commit()
                con.close()

                messagebox.showinfo("Éxito", "✅ Vehículo agregado correctamente.")
                ventana.destroy()

            except ValueError:
                messagebox.showerror("Error", "❌ Año y Cantidad deben ser números enteros.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=15)

    # =====================================================
    # ELIMINAR VEHÍCULO
    # =====================================================
    def eliminar_auto(self):
        id_auto = simpledialog.askstring("Eliminar vehículo", "Ingrese el ID del vehículo:")
        if id_auto:
            try:
                con = sqlite3.connect("gestion_empresarial.db")
                cur = con.cursor()
                cur.execute("DELETE FROM VEHICULOS WHERE id = ?", (id_auto,))
                if cur.rowcount == 0:
                    messagebox.showwarning("No encontrado", "⚠️ No existe ningún vehículo con ese ID.")
                else:
                    con.commit()
                    messagebox.showinfo("Éxito", "✅ Vehículo eliminado exitosamente.")
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        else:
            messagebox.showinfo("Cancelado", "Operación cancelada.")

    # =====================================================
    # EDITAR VEHÍCULO
    # =====================================================
    def editar_auto(self):
        id_auto = simpledialog.askstring("Editar vehículo", "Ingrese el ID del vehículo a editar:")
        if not id_auto:
            return
        messagebox.showinfo("Editar", f"Función para editar vehículo con ID {id_auto} (en desarrollo).")

    # =====================================================
    # BUSCAR VEHÍCULO
    # =====================================================
    def buscar_auto(self):
        criterio = simpledialog.askstring("Buscar", "Ingrese el modelo o marca:")
        if not criterio:
            return

        try:
            con = sqlite3.connect("gestion_empresarial.db")
            cur = con.cursor()
            cur.execute("""
                SELECT * FROM VEHICULOS WHERE marca LIKE ? OR modelo LIKE ?
            """, (f"%{criterio}%", f"%{criterio}%"))
            resultados = cur.fetchall()
            con.close()

            if not resultados:
                messagebox.showinfo("Sin resultados", "❌ No se encontraron coincidencias.")
                return

            # Mostrar resultados en ventana
            self.mostrar_resultados_busqueda(resultados, criterio)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def mostrar_resultados_busqueda(self, resultados, criterio):
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Resultados de búsqueda: {criterio}")
        ventana.geometry("800x400")

        columnas = ("ID", "Marca", "Modelo", "Año", "Tipo", "Cantidad", "Uso")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=100)
        for fila in resultados:
            tabla.insert("", "end", values=fila)
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # =====================================================
    # ADMINISTRADOR
    # =====================================================
    def funciones_admin(self):
        if self.cargo.lower() != "administrador":
            messagebox.showwarning("Acceso denegado", "🚫 Solo los administradores pueden acceder a esta sección.")
            return

        clave_correcta = "clave_admin456"
        for _ in range(3):
            clave_ingresada = simpledialog.askstring("Validación", "Ingrese la clave de administrador:", show="*")
            if clave_ingresada == clave_correcta:
                messagebox.showinfo("Acceso concedido", "✅ Bienvenido al panel administrativo.")
                AdminApp().mainloop()
                return
            else:
                messagebox.showerror("Error", "❌ Clave incorrecta.")
        messagebox.showwarning("Bloqueado", "🚨 Ha superado el límite de intentos.")

    # =====================================================
    # CERRAR SESIÓN
    # =====================================================
    def cerrar_sesion(self):
        confirmar = messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?")
        if confirmar:
            self.destroy()
            self.parent.deiconify()
