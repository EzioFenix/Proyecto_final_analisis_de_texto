import os
import time
import random

from config import Config
from baseDatos import BaseDatos
from scraping import Scraping


def obtener_archivos_json()->list:
    carpeta = "Comentarios_Profesores"
    archivos_json = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta=os.path.join(carpeta,archivo)
            archivos_json.append(ruta)

    return archivos_json



def retardo_aleatorio():
    """Genera un retardo  de 1 5 minutos de retardo
    """
    minutos = random.randint(0, 1)
    segundos = minutos * 30
    time.sleep(segundos)
    print("Retardo completado.")


def ExtraerNombres_links_profes(nombre_archivo:str)->tuple[list[str], list[str]]:
    """Extra los nombres de profesores y links del archivo profesores.txt

    Args:
        nombre_archivo (str): profesores.txt

    Returns:
        tuple[list[str], list[str]]: lista[lista_textp],lista[lista_links]
    """
    # Primero, inicializamos las listas vacías
    lista_texto:list[str] = []
    lista_links:list[str] = []

    # Abrimos el archivo y leemos línea por línea
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for line in f:
            # Quitamos los espacios al principio y al final
            line = line.strip()
            # Si la línea comienza con "Texto:", la agregamos a la lista de texto
            if line.startswith('Texto:'):
                # Quitamos el "Texto:" al principio y lo agregamos a la lista
                lista_texto.append(line[6:])
            # Si la línea comienza con "href:", la agregamos a la lista de links
            elif line.startswith('href:'):
                # Quitamos el "href:" al principio y lo agregamos a la lista
                lista_links.append(line[5:])

    # Devolvemos las dos listas
    return lista_texto, lista_links
        

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
    lista_texto:list[str]
    lista_links:list[str]

    configuracion = Config()
    configuracion.iniciarConfig()

    db=BaseDatos(configuracion.archivo_db)

    mostrar_menu()
    opcion=int(input(":: ").strip())

    if opcion==0: # salir
        pass
    elif opcion==1: # modo scraping
        print(1)
        lista_texto,lista_links=ExtraerNombres_links_profes(configuracion.archivoProfesores)
        print(lista_links[0])

        
        while(configuracion.numArchivosJson < 2036):
            i=configuracion.numArchivosJson
            nombre_Profe_Actual=lista_texto[i]
            url_Actual=lista_links[i]

            scramer=Scraping(url_Actual,nombre_Profe_Actual,configuracion.carpetaGuardadoJSON)

            # Scrapeo con exito y guardo el archivo
            if (scramer.scrapear()==True):
                db.actualizar_fecha_profesor(scramer.nombreProfesor)
                configuracion.numArchivosJson+=1
                
                #retardo_aleatorio()
            else:
                db.actualizar_fecha_profesor(scramer.nombreProfesor)
                configuracion.numArchivosJson+=1
                configuracion.numMaxProfesores-=1
            configuracion.guardar_configuracion()
                

            
main()