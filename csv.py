import csv

class MiObjeto:
    def __init__(self, atributo1, atributo2, atributo3):
        self.atributo1 = atributo1
        self.atributo2 = atributo2
        self.atributo3 = atributo3

# Crear una lista de objetos
objetos = [
    MiObjeto("valor1", "valor2", "valor3"),
    MiObjeto("valor4", "valor5", "valor6"),
    MiObjeto("valor7", "valor8", "valor9")
]

# Abrir el archivo en modo de escritura
with open('archivo.csv', 'w', newline='') as archivo_csv:
    # Crear un objeto csv.writer
    escritor_csv = csv.writer(archivo_csv, delimiter=',')

    # Escribir los encabezados si es necesario
    escritor_csv.writerow(['Atributo 1', 'Atributo 2', 'Atributo 3'])

    # Escribir los valores de los atributos de los objetos
    for objeto in objetos:
        escritor_csv.writerow([objeto.atributo1, objeto.atributo2, objeto.atributo3])
