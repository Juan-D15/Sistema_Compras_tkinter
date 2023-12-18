import tkinter as tk
from tkinter import ttk, messagebox
import pickle, urls


class Clientes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Clientes")

        # Fuentes de texto y urls
        self.fuente_texto = ("Exo 2 Medium", 11)
        self.url_clientes = (
            "Sistema_Compras_TK/Archivos guardados/datos_tabla_Clientes.pkl"
        )

        # Definición de atributos
        self.tabla_c = None
        self.nit_c_entry = None
        self.nombre_c_entry = None
        self.telefono_c_entry = None
        self.direccion_c_entry = None

        self.create_widgets()
        self.cargar_datos()

    def create_widgets(self):
        titulo = tk.Label(
            self.ventana, text="Lista de Clientes", font=("Exo 2 ExtraBold", 15)
        )
        titulo.pack(fill="x")

        # Crear una tabla
        self.tabla_c = ttk.Treeview(
            self.ventana,
            columns=("NIT", "Nombre", "Teléfono", "Dirección"),
            show="headings",
        )
        self.tabla_c.heading("NIT", text="NIT")
        self.tabla_c.heading("Nombre", text="Nombre")
        self.tabla_c.heading("Teléfono", text="Teléfono")
        self.tabla_c.heading("Dirección", text="Dirección")
        self.tabla_c.pack(padx=20, pady=20)

        # Se llama al metodo de la fila seleccionada
        self.tabla_c.bind("<<TreeviewSelect>>", self.fila_seleccionada)

        # Crear un bloque
        frame = tk.Frame(self.ventana)
        frame.pack()

        # Crear un bloque Label
        cliente_info = tk.LabelFrame(frame, text="Clientes", font=self.fuente_texto)
        cliente_info.grid(row=0, column=0, padx=20, pady=20)

        # Crear un label dentro del labelframe
        nit_c = tk.Label(cliente_info, text="NIT", font=self.fuente_texto)
        nit_c.grid(row=0, column=0)

        nombre_c = tk.Label(cliente_info, text="Nombre", font=self.fuente_texto)
        nombre_c.grid(row=0, column=1)

        telefono_c = tk.Label(cliente_info, text="Teléfono", font=self.fuente_texto)
        telefono_c.grid(row=0, column=2)

        direccion_c = tk.Label(cliente_info, text="Dirección", font=self.fuente_texto)
        direccion_c.grid(row=0, column=3)

        # Entradas de datos
        letras = self.ventana.register(validacion_solo_letras)
        numeros = self.ventana.register(validacion_solo_numeros)

        self.nit_c_entry = tk.Entry(
            cliente_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.nit_c_entry.grid(row=1, column=0, padx=5, pady=5)

        self.nombre_c_entry = tk.Entry(
            cliente_info, validate="key", validatecommand=(letras, "%S")
        )
        self.nombre_c_entry.grid(row=1, column=1, padx=5, pady=5)

        self.telefono_c_entry = tk.Entry(
            cliente_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.telefono_c_entry.grid(row=1, column=2, padx=5, pady=5)

        self.direccion_c_entry = tk.Entry(cliente_info)
        self.direccion_c_entry.grid(row=1, column=3, padx=5, pady=5)
        # Botones
        btn_modificar_c = tk.Button(
            cliente_info,
            text="Modificar",
            font=self.fuente_texto,
            command=self.modificar_C,
            cursor="hand2",
        )
        btn_modificar_c.grid(row=2, column=1, padx=5)

        btn_eliminar_c = tk.Button(
            cliente_info,
            text="Eliminar",
            font=self.fuente_texto,
            command=self.eliminar_C,
            cursor="hand2",
        )
        btn_eliminar_c.grid(row=2, column=2, padx=5)

    # Metodos para guardar y cargar datos de la tabla
    def guardar_datos(self):
        datos = [
            self.tabla_c.item(item)["values"] for item in self.tabla_c.get_children()
        ]
        with open(urls.url_clientes, "wb") as file:
            pickle.dump(datos, file)

    def cargar_datos(self):
        try:
            with open(urls.url_clientes, "rb") as file:
                datos = pickle.load(file)
                for dato in datos:
                    self.tabla_c.insert("", tk.END, values=dato)
        except FileNotFoundError:
            pass

    # Metodos para cargar los datos de nit y telefono de los clientes
    def cargar_nit_clientes(self):
        try:
            with open(urls.url_clientes, "rb") as file:
                datos = pickle.load(file)
                codigos_nits = [dato[0] for dato in datos]
                return codigos_nits
        except FileNotFoundError:
            return []

    def cargar_telefonos_clientes(self):
        try:
            with open(urls.url_clientes, "rb") as file:
                datos = pickle.load(file)
                codigos_nits = [dato[2] for dato in datos]
                return codigos_nits
        except FileNotFoundError:
            return []

    # Metodo para obtener los datos de la fila seleccionada y los coloca en los campos respectivos
    def fila_seleccionada(self, event):
        selected_items = self.tabla_c.selection()
        # Si no hay elementos seleccionados
        if not selected_items:
            return
        item = selected_items[0]
        datos = self.tabla_c.item(item)["values"]

        # Llena los campos con los datos de la fila seleccionada
        self.nit_c_entry.delete(0, tk.END)
        self.nit_c_entry.insert(0, datos[0])

        self.nombre_c_entry.delete(0, tk.END)
        self.nombre_c_entry.insert(0, datos[1])

        self.telefono_c_entry.delete(0, tk.END)
        self.telefono_c_entry.insert(0, datos[2])

        self.direccion_c_entry.delete(0, tk.END)
        self.direccion_c_entry.insert(0, datos[3])

    # Metodos para eliminar, modificar y colocar datos en la tabla
    def eliminar_C(self):
        item_seleccionado = self.tabla_c.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        self.tabla_c.delete(dato)
        self.guardar_datos()

    def modificar_C(self):
        item_seleccionado = self.tabla_c.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        nit = self.nit_c_entry.get()
        nom = self.nombre_c_entry.get()
        tel = self.telefono_c_entry.get()
        direc = self.direccion_c_entry.get()

        if nit and nom and tel and direc:
            self.tabla_c.item(dato, values=(nit, nom, tel, direc))
            self.nit_c_entry.delete(0, tk.END)
            self.nombre_c_entry.delete(0, tk.END)
            self.telefono_c_entry.delete(0, tk.END)
            self.direccion_c_entry.delete(0, tk.END)
            self.guardar_datos()

    # Metodo para insertar los datos en la tabla
    def insertar_en_tabla(self, nit, nombre, telefono, direccion):
        self.tabla_c.insert("", tk.END, values=(nit, nombre, telefono, direccion))
        self.guardar_datos()

    # Metodo para verificar los datos de los clientes
    def verificar_datos_clientes(self, nit, nombre, telefono, direccion):
        nits_clientes = [str(nit) for nit in self.cargar_nit_clientes()]
        print(f"Nit Clientes: {nits_clientes}")

        tel_clientes = [str(tel) for tel in self.cargar_telefonos_clientes()]

        if nit not in nits_clientes:
            if telefono in tel_clientes:
                messagebox.showwarning("Advertencia", "El teléfono ya existe")
                return False

            self.insertar_en_tabla(nit, nombre, telefono, direccion)
            self.guardar_datos()
            return True
        else:
            for item in self.tabla_c.get_children():
                datos = self.tabla_c.item(item)["values"]

                print("Datos clientes: ", datos)

                if str(datos[0]) == str(nit) and str(datos[1]) == str(nombre):
                    if datos[2] != telefono or datos[3] != direccion:
                        nuevo_telefono = telefono
                        nueva_direccion = direccion
                    else:
                        nuevo_telefono = datos[2]
                        nueva_direccion = datos[3]

                    self.tabla_c.item(
                        item,
                        values=(datos[0], datos[1], nuevo_telefono, nueva_direccion),
                    )
                    self.guardar_datos()
                    return True
            messagebox.showerror("Error", "El NIT ya existe")
            return False


# Metodo para que solo permita letras y espacios
def validacion_solo_letras(char):
    return char.isalpha() or char in (" ",)


# Metodo para que solo permita numeros
def validacion_solo_numeros(char):
    return char.isdigit()


# Inicializa el interfaz
def mostrar_ventana_clientes():
    ventana = tk.Toplevel()
    Clientes(ventana)
    ventana.mainloop()
