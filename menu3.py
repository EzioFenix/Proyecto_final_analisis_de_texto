import os
import glob
import json
import csv
from comentario import *

def listaJsons_comentarios(carpeta:str)->list[str]:
    """Obtiene los archivos json de los comentarios de profesores

    Args:
        carpeta (str): _description_

    Returns:
        list[str]: _description_
    """

    # Creamos la ruta completa para buscar los archivos json
    ruta = os.path.join(carpeta, '*.json')

    # Usamos glob para encontrar todos los archivos que coincidan
    archivos_json = glob.glob(ruta)

    # Imprimimos cuántos archivos JSON encontramos
    #print(f'Se encontraron {len(archivos_json)} archivos JSON en la carpeta {carpeta}.')

    # Imprimimos la ruta completa de cada archivo JSON
    return archivos_json


def leer_json(ruta:str)->list[dict]:
    """suponinendo que cada archivo json

    Args:
        ruta (str): ruta del archivo a extraer

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        list[dict]: lista de diccionarios (comentarios sin procesar)
    """
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

def comentarios_To_Csv(listaComentarios:list[Comentario]):
    commen:Comentario
    sentimientos=["bueno","malo","fácil","díficil"]

    carpeta = "training"

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta=os.path.join(carpeta,"input.csv")

    with open(ruta, 'w', newline='',encoding="utf-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv, delimiter=',')

        # Escribir los encabezados si es necesario
        escritor_csv.writerow(["review", "sentiment"])

        for commen in  listaComentarios:

            if commen.comments=="[Comentario esperando revisión]" or commen.comments.strip()=="":
                pass
            else:

                review=commen.comments
                sentiment=""
                if float(commen.score_facilidad)<=5.0:
                    sentiment+= sentimientos[3] +"+" #dificil
                else:
                    sentiment+= sentimientos[2] +"+"
                
                """
                if float(commen.score_general) <= 5.0:
                    sentiment+= sentimientos[1]
                else:
                    sentiment += sentimientos[0]

                """

                # Escribir los valores de los atributos de los objetos
                escritor_csv.writerow([review, sentiment])
    print("ok")



def main():
    comentariosNormal:list[Comentario]=[]

    lista_archivos_Json=listaJsons_comentarios('comentarios_profesores')

    for rutaArchivo in lista_archivos_Json:

        #convierte un archivo en comentarios json
        comentariosJson=leer_json(rutaArchivo)
        for comentarioJSon in comentariosJson:
            normal=Comentario.from_dict(comentarioJSon)
            comentariosNormal.append(normal)

    comentarios_To_Csv(comentariosNormal)
    #print(comentariosNormal[0].comments)


    #print(lista[0])

main()

