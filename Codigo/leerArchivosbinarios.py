import pickle


# Abre el archivo en modo lectura binaria "rb"
def datosClientes():
    with open("Proyecto/Archivos guardados/datos_tabla_Clientes.pkl", "rb") as file:
        return pickle.load(file)


# Imprime el contenido del archivo en consola
for dato in datosClientes():
    print(dato)
