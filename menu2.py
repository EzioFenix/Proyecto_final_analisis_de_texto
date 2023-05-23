import os
import json

from config import Config
from baseDatos import BaseDatos





def obtener_archivos_json():
    carpeta = "Comentarios_Profesores"
    archivos_json = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            archivos_json.append(archivo)

    cantidad_archivos = len(archivos_json)

    return cantidad_archivos, archivos_json

# Llamada a la función
#cantidad, archivos = obtener_archivos_json()









        

        


def mostrar_menu():
    """Muestra las opciones para inciar el programa
    """
    opciones = {
        0: "salir",
        1: "modo scraping",
        2: "modo pregunta"
    }

    print("===== MENÚ =====")
    for key, value in opciones.items():
        opcion_centralizada = f"{key}: {value.center(15)}"
        print(opcion_centralizada)
    print("================")


def main():
    configuracion = Config()
    configuracion.iniciarConfig()

    db=BaseDatos(configuracion.archivo_db)

    mostrar_menu()
    opcion=int(input(":: ").strip())

    if opcion==0: # salir
        pass
    elif opcion==1: # modo scraping
        
        while(configuracion.numArchivosJson < configuracion.numMaxProfesores):
            

main()
