import tkinter as tk
from tkinter import ttk, messagebox
import pickle, urls


class Articulos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Artículos")
        # Fuentes de texto
        self.fuente_texto = ("Exo 2 Medium", 11)

        # Definición de atributos
        self.tabla_a = None
        self.codigo_a_entry = None
        self.codigo_p_entry = None
        self.nombre_a_entry = None
        self.cantidad_a_entry = None
        self.preciou_a_entry = None
        self.descripcion_a_entry = None

        self.crear_interfaz()
        self.cargar_datos()

    # Crea los elementos del interfaz
    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana, text="Lista de Artículos", font=("Exo 2 ExtraBold", 15)
        )
        titulo.pack(fill="x")

        # Crea una tabla
        self.tabla_a = ttk.Treeview(
            self.ventana,
            columns=(
                "Código Artículo",
                "Código Proveedor",
                "Nombre",
                "Cantidad",
                "Precio Unitario (Q)",
                "Descripción",
            ),
            show="headings",
        )
        self.tabla_a.heading("Código Artículo", text="Código Artículo")
        self.tabla_a.heading("Código Proveedor", text="Código Proveedor")
        self.tabla_a.heading("Nombre", text="Nombre")
        self.tabla_a.heading("Cantidad", text="Cantidad")
        self.tabla_a.heading("Precio Unitario (Q)", text="Precio Unitario (Q)")
        self.tabla_a.heading("Descripción", text="Descripción")
        self.tabla_a.pack(padx=20, pady=20)

        # Se llama al metodo de fila seleccionada
        self.tabla_a.bind("<<TreeviewSelect>>", self.fila_seleccionada)

        # Crea un bloque
        frame = tk.Frame(self.ventana)
        frame.pack()

        # Crea un Label frame dentro del bloque
        articulos_info = tk.LabelFrame(frame, text="Artículos", font=self.fuente_texto)
        articulos_info.grid(row=0, column=0, padx=20, pady=20)

        # Crea un Label dentro del labelframe
        codigo_a = tk.Label(
            articulos_info, text="Código Artículo", font=self.fuente_texto
        )
        codigo_a.grid(row=0, column=0)

        codigo_p = tk.Label(
            articulos_info, text="Código Proveedor", font=self.fuente_texto
        )
        codigo_p.grid(row=0, column=1)

        nombre_a = tk.Label(articulos_info, text="Nombre", font=self.fuente_texto)
        nombre_a.grid(row=0, column=2)

        cantidad_a = tk.Label(articulos_info, text="Cantidad", font=self.fuente_texto)
        cantidad_a.grid(row=2, column=0)

        preciou_a = tk.Label(
            articulos_info, text="Precio Unitario", font=self.fuente_texto
        )
        preciou_a.grid(row=2, column=1)

        descripcion_a = tk.Label(
            articulos_info, text="Descripción", font=self.fuente_texto
        )
        descripcion_a.grid(row=2, column=2)

        # Entradas de datos
        numeros = self.ventana.register(validacion_solo_numeros)

        self.codigo_a_entry = tk.Entry(
            articulos_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.codigo_a_entry.grid(row=1, column=0, pady=10)

        self.codigo_p_entry = tk.Entry(
            articulos_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.codigo_p_entry.grid(row=1, column=1)

        self.nombre_a_entry = tk.Entry(articulos_info)
        self.nombre_a_entry.grid(row=1, column=2)

        self.cantidad_a_entry = tk.Entry(
            articulos_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.cantidad_a_entry.grid(row=3, column=0)

        self.preciou_a_entry = tk.Entry(
            articulos_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.preciou_a_entry.grid(row=3, column=1)

        self.descripcion_a_entry = tk.Entry(articulos_info)
        self.descripcion_a_entry.grid(row=3, column=2)

        # Botones
        btn_agregar_P = tk.Button(
            articulos_info,
            text="Agregar",
            font=self.fuente_texto,
            command=self.agregar_P,
            cursor="hand2",
        )
        btn_agregar_P.grid(row=4, column=0, padx=10, pady=10)

        btn_eliminar_P = tk.Button(
            articulos_info,
            text="Eliminar",
            font=self.fuente_texto,
            command=self.eliminar_P,
            cursor="hand2",
        )
        btn_eliminar_P.grid(row=4, column=1, padx=10, pady=10)

        btn_modificar_P = tk.Button(
            articulos_info,
            text="Modificar",
            font=self.fuente_texto,
            command=self.modificar_P,
            cursor="hand2",
        )
        btn_modificar_P.grid(row=4, column=2, padx=10, pady=10)

    # Metodos de guardar y cargar datos de la tabla
    def guardar_datos(self):
        datos = [
            self.tabla_a.item(item)["values"] for item in self.tabla_a.get_children()
        ]
        with open(urls.url_articulos, "wb") as file:
            pickle.dump(datos, file)

    def cargar_datos(self):
        try:
            with open(urls.url_articulos, "rb") as file:
                datos = pickle.load(file)
                for dato in datos:
                    self.tabla_a.insert("", tk.END, values=dato)
        except FileNotFoundError:
            pass

    # Metodo para cargar el dato de codigos de la tabla de proveedores
    def cargar_codigos_proveedores(self):
        try:
            with open(urls.url_proveedores, "rb") as file:
                datos = pickle.load(file)
                codigos_proveedores = [dato[0] for dato in datos]
                return codigos_proveedores
        except FileNotFoundError:
            return []

    # Metodo para obtener los datos de la fila seleccionada y los coloca en los campos respectivos
    def fila_seleccionada(self, event):
        selected_items = self.tabla_a.selection()
        # Si no hay elementos seleccionados
        if not selected_items:
            return
        item = selected_items[0]
        datos = self.tabla_a.item(item)["values"]

        # Llena los campos con los datos de la fila seleccionada
        self.codigo_a_entry.delete(0, tk.END)
        self.codigo_a_entry.insert(0, datos[0])

        self.codigo_p_entry.delete(0, tk.END)
        self.codigo_p_entry.insert(0, datos[1])

        self.nombre_a_entry.delete(0, tk.END)
        self.nombre_a_entry.insert(0, datos[2])

        self.cantidad_a_entry.delete(0, tk.END)
        self.cantidad_a_entry.insert(0, datos[3])

        self.preciou_a_entry.delete(0, tk.END)
        self.preciou_a_entry.insert(0, datos[4])

        self.descripcion_a_entry.delete(0, tk.END)
        self.descripcion_a_entry.insert(0, datos[5])

    # Metodos de agregar, eliminar y modificar datos en la tabla
    def agregar_P(self):
        cod_a = self.codigo_a_entry.get()
        cod_p = self.codigo_p_entry.get()
        nom = self.nombre_a_entry.get()
        cant = self.cantidad_a_entry.get()
        pru = self.preciou_a_entry.get()
        des = self.descripcion_a_entry.get()

        # Convertir los codigos de los porveedores en tipos de datos str
        codigos_proveedores = [
            str(codigo) for codigo in self.cargar_codigos_proveedores()
        ]
        # Muestra los códigos cargados
        print(f"Códigos de proveedores: {codigos_proveedores}")

        # Verifica si estan llenos todos los campos
        if cod_a and cod_p and nom and cant and pru and des:
            if self.dato_existente(cod_a, nom):
                messagebox.showwarning("Advertencia", "El Artículo ya existe.")
                return

            # Verificar si el codigo ingresado se encuantra en la lista de codigos de los proveedores
            if cod_p not in codigos_proveedores:
                messagebox.showwarning(
                    "Advertencia", "El Código de Proveedor no existe."
                )
                return

            self.tabla_a.insert("", tk.END, values=(cod_a, cod_p, nom, cant, pru, des))
            self.codigo_a_entry.delete(0, tk.END)
            self.codigo_p_entry.delete(0, tk.END)
            self.nombre_a_entry.delete(0, tk.END)
            self.cantidad_a_entry.delete(0, tk.END)
            self.preciou_a_entry.delete(0, tk.END)
            self.descripcion_a_entry.delete(0, tk.END)
            self.guardar_datos()
        else:
            messagebox.showwarning("Advertencia", "No se han llenado todos los campos")

    def eliminar_P(self):
        item_seleccionado = self.tabla_a.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        self.tabla_a.delete(dato)
        self.guardar_datos()

    def modificar_P(self):
        item_seleccionado = self.tabla_a.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        cod_a = int(self.codigo_a_entry.get())
        cod_p = int(self.codigo_p_entry.get())
        nom = self.nombre_a_entry.get()
        cant = int(self.cantidad_a_entry.get())
        pru = int(self.preciou_a_entry.get())
        des = self.descripcion_a_entry.get()

        if cod_a and cod_p and nom and cant and pru and des:
            self.tabla_a.item(dato, values=(cod_a, cod_p, nom, cant, pru, des))
            self.codigo_a_entry.delete(0, tk.END)
            self.codigo_p_entry.delete(0, tk.END)
            self.nombre_a_entry.delete(0, tk.END)
            self.cantidad_a_entry.delete(0, tk.END)
            self.preciou_a_entry.delete(0, tk.END)
            self.descripcion_a_entry.delete(0, tk.END)
            self.guardar_datos()
        else:
            messagebox.showwarning("Advertencia", "LLene todos los campos")

    # Metodo de verificacion de datos existentes
    def dato_existente(self, cod_a, nom):
        for item in self.tabla_a.get_children():
            datos = self.tabla_a.item(item)["values"]
            if str(datos[0]) == str(cod_a) or str(datos[2]) == str(nom):
                return True
        return False

    # Metodo para verificar si el articulo existe y actualizar la cantidad de articulos
    def verificar_y_actualizar_articulo(self, cod_articulo, cantidad):
        for item in self.tabla_a.get_children():
            # Colca los datos de cada fila en una lista
            datos = self.tabla_a.item(item)["values"]

            print("Datos Articulos: ", datos)  # Imprime la lista obtenida

            if str(datos[0]) == cod_articulo:  # Si el artículo existe
                nueva_cantidad = datos[3] - cantidad  # Le resta la cantidad ingresada
                if nueva_cantidad < 0:
                    messagebox.showwarning(
                        "Advertencia", "No hay suficientes artículos en stock."
                    )
                    return
                elif nueva_cantidad == 0:
                    messagebox.showwarning("Advertencia", "El artículo se ha agotado.")

                # Al precio unitario le multiplica la cantidad ingresada
                precio_unitario = datos[4]
                total = precio_unitario * cantidad
                nom_articulo = datos[2]
                # Agrega los nuevos datos a la tabla
                self.tabla_a.item(
                    item,
                    values=(
                        datos[0],
                        datos[1],
                        datos[2],
                        nueva_cantidad,
                        datos[4],
                        datos[5],
                    ),
                )
                self.guardar_datos()
                return total, precio_unitario, nom_articulo

        messagebox.showwarning("Advertencia", "El artículo no existe")

    # Metodo si se cancela la factura se reintegre la cantidad del articulo
    def reintegrar_articulo(self, articulo, cantidad):
        for item in self.tabla_a.get_children():
            # Colca los datos de cada fila en una lista
            datos = self.tabla_a.item(item)["values"]

            print("Datos Articulos: ", datos)  # Imprime la lista obtenida

            if datos[2] == articulo:  # Si el artículo existe
                nueva_cantidad = datos[3] + cantidad

                self.tabla_a.item(
                    item,
                    values=(
                        datos[0],
                        datos[1],
                        datos[2],
                        nueva_cantidad,
                        datos[4],
                        datos[5],
                    ),
                )
                self.guardar_datos()


# Metodo para que solo permita numeros
def validacion_solo_numeros(char):
    return char.isdigit()


# Inicializa el interfaz
def mostrar_ventana_articulos():
    ventana = tk.Toplevel()
    Articulos(ventana)
    ventana.mainloop()
