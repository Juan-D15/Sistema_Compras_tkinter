import tkinter as tk
from tkinter import ttk, messagebox
import pickle, urls


class Empleados:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Empleados")

        # Fuentes de texto
        self.fuente_texto = ("Exo 2 Medium", 11)

        # Definición de atributos
        self.tabla_e = None
        self.id_e_entry = None
        self.nombre_e_entry = None
        self.puesto_e_entry = None

        self.create_widgets()
        self.cargar_datos()

    def create_widgets(self):
        titulo = tk.Label(
            self.ventana, text="Lista de Empleados", font=("Exo 2 ExtraBold", 15)
        )
        titulo.pack(fill="x")

        # Crear una tabla
        self.tabla_e = ttk.Treeview(
            self.ventana,
            columns=("Id Empleado", "Nombre", "Puesto"),
            show="headings",
        )
        self.tabla_e.heading("Id Empleado", text="Id Empleado")
        self.tabla_e.heading("Nombre", text="Nombre")
        self.tabla_e.heading("Puesto", text="Puesto")
        self.tabla_e.pack(padx=20, pady=20)

        # Se llama al metodo de la fila seleccionada
        self.tabla_e.bind("<<TreeviewSelect>>", self.fila_seleccionada)

        # Crear un bloque
        frame = tk.Frame(self.ventana)
        frame.pack()

        # Crear un bloque Label
        empleados_info = tk.LabelFrame(frame, text="Empleados", font=self.fuente_texto)
        empleados_info.grid(row=0, column=0, padx=20, pady=20)

        # Crear un label dentro del labelframe
        id_e = tk.Label(empleados_info, text="Id Empleado", font=self.fuente_texto)
        id_e.grid(row=0, column=0)

        nombre_e = tk.Label(empleados_info, text="Nombre", font=self.fuente_texto)
        nombre_e.grid(row=0, column=1)

        puesto_e = tk.Label(empleados_info, text="Puesto", font=self.fuente_texto)
        puesto_e.grid(row=0, column=2)

        # Entradas de datos
        letras = self.ventana.register(validacion_solo_letras)
        numeros = self.ventana.register(validacion_solo_numeros)

        self.id_e_entry = tk.Entry(
            empleados_info, validate="key", validatecommand=(numeros, "%S")
        )
        self.id_e_entry.grid(row=1, column=0, pady=10)

        self.nombre_e_entry = tk.Entry(
            empleados_info, validate="key", validatecommand=(letras, "%S")
        )
        self.nombre_e_entry.grid(row=1, column=1)

        self.puesto_e_entry = tk.Entry(
            empleados_info, validate="key", validatecommand=(letras, "%S")
        )
        self.puesto_e_entry.grid(row=1, column=2)

        # Botones
        btn_agregar_P = tk.Button(
            empleados_info,
            text="Agregar",
            font=self.fuente_texto,
            command=self.agregar_P,
            cursor="hand2",
        )
        btn_agregar_P.grid(row=2, column=0, padx=10)

        btn_eliminar_P = tk.Button(
            empleados_info,
            text="Eliminar",
            font=self.fuente_texto,
            command=self.eliminar_P,
            cursor="hand2",
        )
        btn_eliminar_P.grid(row=2, column=1, padx=10)

        btn_modificar_P = tk.Button(
            empleados_info,
            text="Modificar",
            font=self.fuente_texto,
            command=self.modificar_P,
            cursor="hand2",
        )
        btn_modificar_P.grid(row=2, column=2, padx=10)

    # Métodos para guardar, cargar y manipular datos
    def guardar_datos(self):
        datos = [
            self.tabla_e.item(item)["values"] for item in self.tabla_e.get_children()
        ]
        with open(urls.url_empleados, "wb") as file:
            pickle.dump(datos, file)

    def cargar_datos(self):
        try:
            with open(urls.url_empleados, "rb") as file:
                datos = pickle.load(file)
                for dato in datos:
                    self.tabla_e.insert("", tk.END, values=dato)
        except FileNotFoundError:
            pass

    # Metodo para obtener los datos de la fila seleccionada y los coloca en los campos respectivos
    def fila_seleccionada(self, event):
        selected_items = self.tabla_e.selection()
        # Si no hay elementos seleccionados
        if not selected_items:
            return
        item = selected_items[0]
        datos = self.tabla_e.item(item)["values"]

        # Llena los campos con los datos de la fila seleccionada
        self.id_e_entry.delete(0, tk.END)
        self.id_e_entry.insert(0, datos[0])

        self.nombre_e_entry.delete(0, tk.END)
        self.nombre_e_entry.insert(0, datos[1])

        self.puesto_e_entry.delete(0, tk.END)
        self.puesto_e_entry.insert(0, datos[2])

    # Metodos de agregar, eliminar y modificar datos en la tabla
    def agregar_P(self):
        ide = self.id_e_entry.get()
        nom = self.nombre_e_entry.get()
        pste = self.puesto_e_entry.get()

        if ide and nom and pste:
            if self.dato_existente(ide, nom):
                messagebox.showwarning("Advertencia", "El empleado ya existe")
                return

            self.tabla_e.insert("", tk.END, values=(ide, nom, pste))
            self.id_e_entry.delete(0, tk.END)
            self.nombre_e_entry.delete(0, tk.END)
            self.puesto_e_entry.delete(0, tk.END)
            self.guardar_datos()
        else:
            messagebox.showwarning("Advertencia", "No se han llenado todos los campos")

    def eliminar_P(self):
        item_seleccionado = self.tabla_e.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        self.tabla_e.delete(dato)
        self.guardar_datos()

    def modificar_P(self):
        item_seleccionado = self.tabla_e.selection()
        if not item_seleccionado:
            return
        dato = item_seleccionado[0]

        ide = self.id_e_entry.get()
        nom = self.nombre_e_entry.get()
        pste = self.puesto_e_entry.get()

        if ide and nom and pste:
            self.tabla_e.item(dato, values=(ide, nom, pste))
            self.id_e_entry.delete(0, tk.END)
            self.nombre_e_entry.delete(0, tk.END)
            self.puesto_e_entry.delete(0, tk.END)
            self.guardar_datos()
        else:
            messagebox.showwarning("Advertencia", "LLene todos los campos")

    # Metodo para verificar si los datos existen
    def dato_existente(self, ide, nom):
        for item in self.tabla_e.get_children():
            datos = self.tabla_e.item(item)["values"]
            if str(datos[0]) == str(ide) or str(datos[1]) == str(nom):
                return True
        return False

    # Metodo para verificar quien tiene el puesto de cajero
    def verificar_empleado_cajero(self, empleado):
        for item in self.tabla_e.get_children():
            datos = self.tabla_e.item(item)["values"]
            print("datos empleados: ", datos)

            if datos[1] == empleado and datos[2] == "cajero":
                return False
        return True


# Metodo para que solo permita letras y espacios
def validacion_solo_letras(char):
    return char.isalpha() or char in (" ",)


# Metodo para que solo permita numeros
def validacion_solo_numeros(char):
    return char.isdigit()


def mostrar_ventana_empleados():
    ventana = tk.Toplevel()
    Empleados(ventana)
    ventana.mainloop()
