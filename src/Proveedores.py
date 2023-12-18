import tkinter as tk
from tkinter import ttk, messagebox
import pickle, urls


class Proveedores:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Proveedores")

        # Fuentes de texto
        self.fuente_texto = ("Exo 2 Medium", 11)

        # Definición de atributos
        self.tabla_p = None
        self.codigo_p_entry = None
        self.nit_p_entry = None
        self.nombre_p_entry = None
        self.direccion_p_entry = None
        self.telefono_p_entry = None

        self.create_widgets()
        self.cargar_datos()

    def create_widgets(self):
        titulo = tk.Label(
            self.ventana, text="Lista de Proveedores", font=("Exo 2 ExtraBold", 15)
        )
        titulo.pack(fill="x")

        # Crear una tabla
        self.tabla_p = ttk.Treeview(
            self.ventana,
            columns=("Código", "NIT", "Nombre", "Dirección", "Teléfono"),
            show="headings",
        )
        self.tabla_p.heading("Código", text="Código")
        self.tabla_p.heading("NIT", text="NIT")
        self.tabla_p.heading("Nombre", text="Nombre")
        self.tabla_p.heading("Dirección", text="Dirección")
        self.tabla_p.heading("Teléfono", text="Teléfono")
        self.tabla_p.pack(padx=20, pady=20)

        # Se llama al metodo de la fila seleccionada
        self.tabla_p.bind("<<TreeviewSelect>>", self.fila_seleccionada)

        # Crear un bloque
        frame = tk.Frame(self.ventana)
        frame.pack()

        # Crear un bloque Label
        proveedores_info = tk.LabelFrame(
            frame, text="Proveedores", font=self.fuente_texto
        )
        proveedores_info.grid(row=0, column=0, padx=20, pady=20)

        # Crear un label dentro del labelframe
        codigo_p = tk.Label(proveedores_info, text="Código", font=self.fuente_texto)
        codigo_p.grid(row=0, column=0)

        nit_p = tk.Label(proveedores_info, text="NIT", font=self.fuente_texto)
        nit_p.grid(row=0, column=1)

        nombre_p = tk.Label(proveedores_info, text="Nombre", font=self.fuente_texto)
        nombre_p.grid(row=0, column=2)

        direccion_p = tk.Label(
            proveedores_info, text="Dirección", font=self.fuente_texto
        )
        direccion_p.grid(row=0, column=3)

        telefono_p = tk.Label(proveedores_info, text="Teléfono", font=self.fuente_texto)
        telefono_p.grid(row=0, column=4)

        # Entradas de datos
        numeros = self.ventana.register(validacion_solo_numeros)

        self.codigo_p_entry = tk.Entry(
            proveedores_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.codigo_p_entry.grid(row=1, column=0, pady=10)

        self.nit_p_entry = tk.Entry(
            proveedores_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.nit_p_entry.grid(row=1, column=1)

        self.nombre_p_entry = tk.Entry(proveedores_info)
        self.nombre_p_entry.grid(row=1, column=2)

        self.direccion_p_entry = tk.Entry(proveedores_info)
        self.direccion_p_entry.grid(row=1, column=3)

        self.telefono_p_entry = tk.Entry(proveedores_info)
        self.telefono_p_entry.grid(row=1, column=4)

        # Botones
        btn_agregar_P = tk.Button(
            proveedores_info,
            text="Agregar",
            font=self.fuente_texto,
            command=self.agregar_P,
            cursor="hand2",
        )
        btn_agregar_P.grid(row=2, column=1, padx=10)

        btn_eliminar_P = tk.Button(
            proveedores_info,
            text="Eliminar",
            font=self.fuente_texto,
            command=self.eliminar_P,
            cursor="hand2",
        )
        btn_eliminar_P.grid(row=2, column=2, padx=10)

        btn_modificar_P = tk.Button(
            proveedores_info,
            text="Modificar",
            font=self.fuente_texto,
            command=self.modificar_P,
            cursor="hand2",
        )
        btn_modificar_P.grid(row=2, column=3, padx=10)

    # Metodos para guardar y cargar datos de la tabla
    def guardar_datos(self):
        datos = [
            self.tabla_p.item(item)["values"] for item in self.tabla_p.get_children()
        ]
        with open(urls.url_proveedores, "wb") as file:
            pickle.dump(datos, file)

    def cargar_datos(self):
        try:
            with open(urls.url_proveedores, "rb") as file:
                datos = pickle.load(file)
                for dato in datos:
                    self.tabla_p.insert("", tk.END, values=dato)
        except FileNotFoundError:
            pass

    # Metodo para obtener los datos de la fila seleccionada y los coloca en los campos respectivos
    def fila_seleccionada(self, event):
        item_seleccionado = self.tabla_p.selection()
        # Si no hay elementos seleccionados
        if not item_seleccionado:
            return
        item = item_seleccionado[0]
        datos = self.tabla_p.item(item)["values"]

        # Llena los campos con los datos de la fila seleccionada
        self.codigo_p_entry.delete(0, tk.END)
        self.codigo_p_entry.insert(0, datos[0])

        self.nit_p_entry.delete(0, tk.END)
        self.nit_p_entry.insert(0, datos[1])

        self.nombre_p_entry.delete(0, tk.END)
        self.nombre_p_entry.insert(0, datos[2])

        self.direccion_p_entry.delete(0, tk.END)
        self.direccion_p_entry.insert(0, datos[3])

        self.telefono_p_entry.delete(0, tk.END)
        self.telefono_p_entry.insert(0, datos[4])

    # Métodos para guardar, cargar y modificar datos
    def agregar_P(self):
        cod = self.codigo_p_entry.get()
        nit = self.nit_p_entry.get()
        nom = self.nombre_p_entry.get()
        dire = self.direccion_p_entry.get()
        tel = self.telefono_p_entry.get()

        if cod and nit and nom and dire and tel:
            if self.dato_existente(cod, nit, nom, tel):
                messagebox.showwarning("Advertencia", "El proveedor ya existe")
                return

            self.tabla_p.insert("", tk.END, values=(cod, nit, nom, dire, tel))
            self.codigo_p_entry.delete(0, tk.END)
            self.nit_p_entry.delete(0, tk.END)
            self.nombre_p_entry.delete(0, tk.END)
            self.direccion_p_entry.delete(0, tk.END)
            self.telefono_p_entry.delete(0, tk.END)
            self.guardar_datos()
        else:
            messagebox.showwarning("Advertencia", "No se han llenado todos los campos")

    def eliminar_P(self):
        item_seleccionado = self.tabla_p.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        self.tabla_p.delete(dato)
        self.guardar_datos()

    def modificar_P(self):
        item_seleccionado = self.tabla_p.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        cod = self.codigo_p_entry.get()
        nit = self.nit_p_entry.get()
        nom = self.nombre_p_entry.get()
        dire = self.direccion_p_entry.get()
        tel = self.telefono_p_entry.get()

        if cod and nit and nom and dire and tel:
            self.tabla_p.item(dato, values=(cod, nit, nom, dire, tel))
            self.codigo_p_entry.delete(0, tk.END)
            self.nit_p_entry.delete(0, tk.END)
            self.nombre_p_entry.delete(0, tk.END)
            self.direccion_p_entry.delete(0, tk.END)
            self.telefono_p_entry.delete(0, tk.END)
            self.guardar_datos()

    # Metodo para verificar si los datos existen
    def dato_existente(self, cod, nit, nom, tel):
        for item in self.tabla_p.get_children():
            datos = self.tabla_p.item(item)["values"]
            if (
                str(datos[0]) == str(cod)
                or str(datos[1]) == str(nit)
                or str(datos[2]) == str(nom)
                or str(datos[4]) == str(tel)
            ):
                return True
        return False


# Metodo para que solo permita numeros
def validacion_solo_numeros(char):
    return char.isdigit()


# Inicializa el interfaz
def mostrar_ventana_proveedores():
    ventana = tk.Toplevel()
    Proveedores(ventana)
    ventana.mainloop()
