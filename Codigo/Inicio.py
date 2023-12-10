import tkinter as tk
import Articulos, Proveedores, Empleados, Clientes, Compras


def iniciar():
    inicio = tk.Tk()
    inicio.title("Farmacia Monja Blanca")

    # Establecer un color de fondo
    inicio.configure(bg="white")
    fuente = ("Exo 2 Medium", 11)

    titulo = tk.Label(
        inicio, text="Monja Blanca", font=("Exo 2 ExtraBold", 15), bg="white"
    )
    titulo.pack(pady=20)

    opciones = tk.Frame(inicio, bg="white")
    opciones.pack(pady=20)

    # Botones
    boton_p = tk.Button(
        opciones,
        text="Proveedores",
        font=fuente,
        command=Proveedores.mostrar_ventana_proveedores,
        cursor="hand2",  # Tipo de cursor
        bg="#374963",  # Color boton
        fg="white",  # Texto blanco
        padx=10,
        pady=5,
    )
    boton_p.grid(row=0, column=0, padx=10)

    boton_a = tk.Button(
        opciones,
        text="Articulos",
        font=fuente,
        command=Articulos.mostrar_ventana_articulos,
        cursor="hand2",
        bg="#374963",  # Color boton
        fg="white",
        padx=10,
        pady=5,
    )
    boton_a.grid(row=0, column=1, padx=10)

    boton_e = tk.Button(
        opciones,
        text="Empleados",
        font=fuente,
        command=Empleados.mostrar_ventana_empleados,
        cursor="hand2",
        bg="#374963",  # Color boton
        fg="white",
        padx=10,
        pady=5,
    )
    boton_e.grid(row=0, column=2, padx=10)

    boton_c = tk.Button(
        opciones,
        text="Clientes",
        font=fuente,
        command=Clientes.mostrar_ventana_clientes,
        cursor="hand2",
        bg="#374963",  # Color boton
        fg="white",
        padx=10,
        pady=5,
    )
    boton_c.grid(row=0, column=3, padx=10)

    boton_co = tk.Button(
        opciones,
        text="Compras",
        font=fuente,
        command=Compras.mostrar_ventana_compras,
        cursor="hand2",
        bg="#374963",  # Color boton
        fg="white",
        padx=10,
        pady=5,
    )
    boton_co.grid(row=0, column=4, padx=10)

    inicio.mainloop()


iniciar()
