import os
import glob
import json
from comentario import *

def cuenta_jsons_en_carpeta(carpeta):
    # Creamos la ruta completa para buscar los archivos json
    ruta = os.path.join(carpeta, '*.json')

    # Usamos glob para encontrar todos los archivos que coincidan
    archivos_json = glob.glob(ruta)

    # Imprimimos cuántos archivos JSON encontramos
    print(f'Se encontraron {len(archivos_json)} archivos JSON en la carpeta {carpeta}.')

    # Imprimimos la ruta completa de cada archivo JSON
    return archivos_json


def leer_json(ruta):
    # Abre el archivo json
    with open(ruta, 'r',encoding="utf-8") as archivo:
        # Lee y deserializa el json a una lista de diccionarios
        datos = json.load(archivo)
        
    # Verifica que los datos sean una lista
    if not isinstance(datos, list):
        raise ValueError('El contenido del archivo JSON no es una lista')
    
    # Verifica que todos los elementos de la lista sean diccionarios
    for elemento in datos:
        if not isinstance(elemento, dict):
            raise ValueError('Uno o más elementos en la lista no son diccionarios')
    
    # Devuelve la lista de diccionarios
    return datos



def main():
    # Test
    comentariosNormal:list[Comentario]=[]
    lista=cuenta_jsons_en_carpeta('comentarios_profesores')
    comentariosJson=leer_json(lista[0])
    for comentarioJSon in comentariosJson:
        normal=Comentario.from_dict(comentarioJSon)
        comentariosNormal.append(normal)

    print(comentariosNormal[0].comments)


    #print(lista[0])

main()

