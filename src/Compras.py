import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from fpdf import FPDF
import Clientes, Articulos, Empleados, urls


class Compras:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Compras")

        # Fuentes de texto y urls
        self.fuente_texto = ("Exo 2 Medium", 11)

        self.numero_factura = self.cargar_numeros_factura()
        self.carrito_compras = []

        self.nit_entry = None
        self.nombre_entry = None
        self.telefono_entry = None
        self.direccion_entry = None
        self.cod_articulo_entry = None
        self.cantidad_entry = None
        self.total_entry = None
        self.empleado_entry = None
        self.no_caja_entry = None
        self.txtarea = None

        self.crear_widgets()

    def crear_widgets(self):
        titulo = tk.Label(
            self.ventana, text="Compras", font=("Exo 2 ExtraBold", 15), bg="#f2f2f2"
        )
        titulo.pack(fill="x")

        # Bloque
        campos = tk.Frame(self.ventana)
        campos.pack()

        # Texto
        nit = tk.Label(campos, text="NIT", font=self.fuente_texto)
        nit.grid(row=0, column=0)

        nombre = tk.Label(campos, text="Nombre", font=self.fuente_texto)
        nombre.grid(row=0, column=1)

        telefono = tk.Label(campos, text="Teléfono", font=self.fuente_texto)
        telefono.grid(row=0, column=2)

        direccion = tk.Label(campos, text="Dirección", font=self.fuente_texto)
        direccion.grid(row=0, column=3)

        articulo = tk.Label(campos, text="Cod. Artículo", font=self.fuente_texto)
        articulo.grid(row=2, column=0)

        cantidad = tk.Label(campos, text="Cantidad", font=self.fuente_texto)
        cantidad.grid(row=2, column=1)

        empleado = tk.Label(campos, text="Cajero", font=self.fuente_texto)
        empleado.grid(row=2, column=2)

        no_caja = tk.Label(campos, text="No. Caja", font=self.fuente_texto)
        no_caja.grid(row=2, column=3)

        total = tk.Label(campos, text="SubTotal", font=self.fuente_texto)
        total.grid(row=4, column=1, columnspan=2, sticky=tk.EW)

        # Entradas
        letras = self.ventana.register(validacion_solo_letras)
        numeros = self.ventana.register(validacion_solo_numeros)

        self.nit_entry = tk.Entry(
            campos, validate="key", validatecommand=(numeros, "%S")
        )
        self.nit_entry.grid(row=1, column=0, padx=5, pady=5)
        self.nit_entry.bind("<Return>", self.autocompletar_campos)

        self.nombre_entry = tk.Entry(
            campos, validate="key", validatecommand=(letras, "%S")
        )
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        self.telefono_entry = tk.Entry(
            campos, validate="key", validatecommand=(numeros, "%S")
        )
        self.telefono_entry.grid(row=1, column=2, padx=5, pady=5)

        self.direccion_entry = tk.Entry(campos)
        self.direccion_entry.grid(row=1, column=3, padx=5, pady=5)

        self.cod_articulo_entry = tk.Entry(
            campos, validate="key", validatecommand=(numeros, "%S")
        )
        self.cod_articulo_entry.grid(row=3, column=0, padx=5, pady=5)

        self.cantidad_entry = tk.Entry(
            campos, validate="key", validatecommand=(numeros, "%S")
        )
        self.cantidad_entry.grid(row=3, column=1, padx=5, pady=5)

        self.empleado_entry = tk.Entry(
            campos, validate="key", validatecommand=(letras, "%S")
        )
        self.empleado_entry.grid(row=3, column=2, padx=5, pady=5)

        self.no_caja_entry = tk.Entry(
            campos, validate="key", validatecommand=(numeros, "%S")
        )
        self.no_caja_entry.grid(row=3, column=3, padx=5, pady=5)

        self.total_entry = tk.Entry(campos)
        self.total_entry.grid(
            row=5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW
        )

        # Area Facturacion
        titulof = tk.Label(
            self.ventana, text="Facturación", font=("Exo 2 ExtraBold", 15), bg="#f2f2f2"
        )
        titulof.pack(fill="x")

        frame_txtarea = tk.Frame(self.ventana)
        frame_txtarea.pack(pady=10)

        scrol_y = tk.Scrollbar(frame_txtarea, orient="vertical")
        self.txtarea = tk.Text(
            frame_txtarea,
            yscrollcommand=scrol_y.set,
            width=50,
            height=20,
        )
        scrol_y.pack(side="right", fill="y")
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill="both", expand=1)

        # Botones
        btn_agregar = tk.Button(
            campos,
            text="Agregar",
            font=self.fuente_texto,
            command=self.enviar_datos_a_clientes,
            cursor="hand2",
        )
        btn_agregar.grid(row=6, column=0, padx=2, pady=2)

        btn_factura = tk.Button(
            campos,
            text="Factura",
            font=self.fuente_texto,
            command=self.generar_factura_txtArea,
            cursor="hand2",
        )
        btn_factura.grid(row=6, column=1, padx=2, pady=2)

        btn_cancelar_factura = tk.Button(
            campos,
            text="Cancelar Factura",
            font=self.fuente_texto,
            command=self.cancelar_factura,
            cursor="hand2",
        )
        btn_cancelar_factura.grid(row=6, column=2, padx=2, pady=2)

        btn_generar_factura = tk.Button(
            campos,
            text="Generar Factura",
            font=self.fuente_texto,
            command=self.generar_factura_pdf,
            cursor="hand2",
        )
        btn_generar_factura.grid(row=6, column=3, padx=2, pady=2)

    # Carga y guarda los numeros de factura
    def cargar_numeros_factura(self):
        try:
            with open(urls.url_noFactura, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return 1

    def guardar_numeros_factura(self):
        with open(urls.url_noFactura, "wb") as file:
            pickle.dump(self.numero_factura, file)

    # Carga los nombres de los empleados que esten en la tabla
    def cargar_nombre_empleados(self):
        try:
            with open(urls.url_empleados, "rb") as file:
                datos = pickle.load(file)
                nombres_emp = [dato[1] for dato in datos]
                return nombres_emp
        except FileNotFoundError:
            return []

    # Carga los datos de los clientes que esten en la tabla
    def cargar_datos_clientes(self):
        with open(urls.url_clientes, "rb") as file:
            return pickle.load(file)

    # Metodo para generar un pdf de la factura
    def generar_factura_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Encabezado
        pdf.cell(200, 10, txt="Farmacia Monja Blanca", ln=True, align="C")
        pdf.cell(200, 10, txt=f"No. Factura: {self.numero_factura}", ln=True)
        pdf.cell(200, 10, txt=f"Cajero: {self.empleado_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"No. Caja: {self.no_caja_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"NIT: {self.nit_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Nombre: {self.nombre_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Teléfono: {self.telefono_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Dirección: {self.direccion_entry.get()}", ln=True)
        pdf.ln(10)  # Espacio

        # Columnas para los artículos
        col_widths = [50, 30, 40, 40]
        total_width = sum(col_widths)
        left_margin = (210 - total_width) / 2
        pdf.set_left_margin(left_margin)

        columns = ["Artículo", "Cantidad", "Precio Unitario (Q)", "Total (Q)"]
        for i, column in enumerate(columns):
            pdf.cell(col_widths[i], 10, txt=column, border=1)
        pdf.ln()

        # Añadir los artículos del carrito al PDF
        for item in self.carrito_compras:
            pdf.cell(col_widths[0], 10, txt=item["articulo"], border=1)
            pdf.cell(col_widths[1], 10, txt=str(item["cantidad"]), border=1)
            pdf.cell(col_widths[2], 10, txt=str(item["precioU"]), border=1)
            pdf.cell(col_widths[3], 10, txt=str(item["total"]), border=1)
            pdf.ln()

        # SubTotal
        pdf.cell(
            sum(col_widths[:3]),
            10,
            txt="SubTotal",
            align="L",
            border=1,
            ln=False,
        )
        # En la columna "Total (Q)" se coloca el valor del SubTotal
        pdf.cell(col_widths[3], 10, txt=str(self.sub_total), border=1)

        # Guardar el PDF
        pdf.output("Proyecto/Facturas PDF/Factura.pdf")

    # Metodo para generar la factura en el txtArea
    def generar_factura_txtArea(self):
        # Limpiar el txtarea
        self.txtarea.config(state="normal")
        self.txtarea.delete(1.0, tk.END)
        self.sub_total = 0

        # Obtener los datos básicos
        nit, nombre, telefono, empleado, direccion = self.obtener_datos()
        self.numero_factura += 1
        self.guardar_numeros_factura()
        # Generar el encabezado de la factura
        factura = "Farmacia Monja Blanca\n\n"
        factura += f"No. Factura: {self.numero_factura}\n"
        factura += f"Cajero: {empleado}\n"
        factura += f"No. Caja: {self.no_caja_entry.get()}\n\n"
        factura += f"NIT: {nit}\n"
        factura += f"Nombre: {nombre}\n"
        factura += f"Teléfono: {telefono}\n"
        factura += f"Dirección: {direccion}\n\n"
        factura += "-" * 50 + "\n"  # Separador

        # Añadir los artículos del carrito a la factura
        for item in self.carrito_compras:
            factura += f"Artículo: {item['articulo']}\n"
            factura += f"Cantidad: {item['cantidad']}\n"
            factura += f"Precio c/u: Q{item['precioU']}\n"
            factura += f"Total: Q{item['total']}\n"
            factura += "-" * 50 + "\n\n"  # Separador
            self.sub_total += item["total"]

        factura += f"SubTotal: Q{self.sub_total}"

        self.total_entry.delete(0, tk.END)  # Limpia el campo Total
        # Inserta SubTotal en el campo Total
        self.total_entry.insert(0, self.sub_total)

        # Colocar la factura en el txtarea
        self.txtarea.insert(tk.END, factura)
        self.txtarea.config(state="disabled")

    # Metodo para cancelar la factura
    def cancelar_factura(self):
        self.txtarea.config(state="normal")
        self.txtarea.delete(1.0, tk.END)
        self.txtarea.config(state="disabled")
        self.total_entry.delete(0, tk.END)

        self.sub_total = 0

        self.numero_factura -= 1
        self.guardar_numeros_factura()

        # Se llama al metodo de reintegrar articulo que se encuantra en la clase Articulos
        ventana_articulos = tk.Toplevel(self.ventana)
        articulos = Articulos.Articulos(ventana_articulos)
        # En cada articulo puesto en el carrito agrega la cantidad que se le quitó
        for item in self.carrito_compras:
            articulo = item["articulo"]
            cantidad = item["cantidad"]
            articulos.reintegrar_articulo(articulo, cantidad)
        ventana_articulos.destroy()
        # Deja la lista de carrito de compras vacia
        self.carrito_compras = []

    # Metodos para obtener los datos de los campos de compras
    def obtener_datos(self):
        nit = self.nit_entry.get()
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        empleado = self.empleado_entry.get()
        direccion = self.direccion_entry.get()
        no_caja = self.no_caja_entry.get()
        # Si todos estan llenos que retorne los datos ingresados en cada campo, si no que lance un mensaje de advertencia
        if nit and nombre and telefono and empleado and no_caja:
            return nit, nombre, telefono, empleado, direccion
        else:
            messagebox.showwarning("Advertencia", "Llene todos los campos")
            return None, None, None, None, None

    def obtener_datos_articulo(self):
        cod_articulo = self.cod_articulo_entry.get()
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese una cantidad válida.")
            return None, None
        return cod_articulo, cantidad

    # Metodo para enviar los datos de los clientes obtenidos a su respectiva tabla
    def enviar_datos_a_clientes(self):
        nit, nombre, telefono, empleado, direccion = self.obtener_datos()

        if None in (nit, nombre, telefono, empleado):
            return

        cod_articulo, cantidad = self.obtener_datos_articulo()

        nombres_empleados = [str(nom) for nom in self.cargar_nombre_empleados()]
        print(f"Nombres empleados: {nombres_empleados}")

        if empleado not in nombres_empleados:
            messagebox.showwarning("Advertencia", "El Empleado no existe")
            return
        else:
            ventana_empleados = tk.Toplevel(self.ventana)
            empleados = Empleados.Empleados(ventana_empleados)
            acceso = empleados.verificar_empleado_cajero(empleado)
            ventana_empleados.destroy()

            if acceso:
                messagebox.showwarning("Advertencia", f"{empleado} No es Cajero")
                return
            else:
                ventana_clientes = tk.Toplevel(self.ventana)
                clientes = Clientes.Clientes(ventana_clientes)
                validar_cliente = clientes.verificar_datos_clientes(
                    nit, nombre, telefono, direccion
                )
                if not validar_cliente:
                    return

                ventana_clientes.destroy()

        if cod_articulo and cantidad is not None:
            ventana_articulos = tk.Toplevel(self.ventana)
            articulos = Articulos.Articulos(ventana_articulos)
            (
                total,
                precio_unitario,
                nom_articulo,
            ) = articulos.verificar_y_actualizar_articulo(
                cod_articulo, cantidad
            )  # Obtiene el total y el precio unitario
            ventana_articulos.destroy()

            # Si se obtuvo un total
            if total is not None:
                # Almacenar articulos en el carrito
                self.carrito_compras.append(
                    {
                        "articulo": nom_articulo,
                        "cantidad": cantidad,
                        "precioU": precio_unitario,
                        "total": total,
                    }
                )

    # Completa los demas campos si en NIT existe
    def autocompletar_campos(self, event):
        nit = self.nit_entry.get()

        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)

        for datos in self.cargar_datos_clientes():
            if str(datos[0]) == nit:
                self.nombre_entry.insert(0, datos[1])
                self.telefono_entry.insert(0, datos[2])
                self.direccion_entry.insert(0, datos[3] if datos[3] is not None else "")


# Metodo para que solo permita letras y espacios
def validacion_solo_letras(char):
    return char.isalpha() or char in (" ",)


# Metodo para que solo permita numeros
def validacion_solo_numeros(char):
    return char.isdigit()


# Inicializa el interfaz
def mostrar_ventana_compras():
    ventana = tk.Tk()
    Compras(ventana)
    ventana.mainloop()
