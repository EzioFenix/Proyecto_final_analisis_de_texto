import requests
from bs4 import BeautifulSoup
from typing import List
import json
from baseDatos import *


class Comentario:
    def __init__(
        self,
        fecha: str,
        score_Total: int,
        materia: str,
        comments: str
        ) -> None:
        
        self.fecha = fecha
        self.score_Total = score_Total
        self.materia = materia
        self.comments = comments
    
    # Este método convierte el objeto en un diccionario
    def to_dict(self):
        return {
            'fecha': self.fecha,
            'score_Total': self.score_Total,
            'materia': self.materia,
            'comments': self.comments
        }

    # Este método estático crea un nuevo objeto Comentario a partir de un diccionario
    @staticmethod
    def from_dict(source):
        return Comentario(
            fecha=source['fecha'],
            score_Total=source['score_Total'],
            materia=source['materia'],
            comments=source['comments']
        )


listaComentarios:List[Comentario]


def scrappingProfesor_SoloUnaPag(url:str,numPagActual:int)->List[Comentario]:
    """Realiza el scraping a una pagina dada de mis profesores.com para obtener los comentarios (sólo a una)

    Args:
        url (str): Url a la que se le realiza la extraccion de comentarios  
        numPagActual (int): Si la página tiene varias paginas paginas de comentarios (1,2,3,4) entonces se pasa este numero

    Returns:
        List[Comentario]: Lista con los comentarios obtenidos
    """
    listaComentarios:List[Comentario]=[]

    print("pagina actual: " + str(numPagActual))
    # Realizar la solicitud GET a la URL
    response = requests.get(url)

    # Crear el objeto BeautifulSoup con el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla por su clase CSS
    tabla = soup.find('table')

    # Verificar si se encontró la tabla
    if tabla:
        # Recorrer las filas de la tabla
        for fila in tabla.find_all('tr')[1:]:
            # Recorrer las celdas de cada fila

            fecha = fila.find('div', class_='date').text.strip()
            score_malo = fila.find_all('span', class_='score')[0].text.strip()
            score_regular = fila.find_all('span', class_='score')[1].text.strip()
            scoreTotal= int((float(score_malo)+float(score_regular))/2)
            materia = fila.find('span', class_='name').text.strip()
            textos_unidos:str
            comments = fila.find('p', class_='commentsParagraph')

            #------------------Etiquetas-------------------------------------------
            tagbox = fila.find('div', class_='tagbox')

            if tagbox:
                textos = [span.text.strip() for span in tagbox.find_all('span')]
                textos_unidos = ', '.join(textos)
            else:
                textos_unidos=""

            # comentario
            if comments:
                textos_unidos+= soup.find('p', class_='commentsParagraph').text.strip()

            nuevoComentario=Comentario(fecha,scoreTotal,materia,textos_unidos)
            listaComentarios.append(nuevoComentario)
            
            # comprobar  que esta recolentando data--------------
            #print("Fecha:", fecha)
            #print("Score total:", scoreTotal)
            #print("Materia:", materia)
            #print("Comentario:", textos_unidos)
            #print('---')
            # comprobar  que esta recolentando data--------------
            
    else:
        print("No se encontró la tabla en la página.")

    return listaComentarios


def scrappingProfesor(url:str):
    response = requests.get(url)
    numPags:int

    listaComentarios:List[Comentario]=[]

    # Crear el objeto BeautifulSoup con el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla por su clase CSS
    # -2  es poruqe el final es una vacia en li
    numPags = int(soup.find_all('li')[-2].text.strip())

    # scraping a las paginas--------------------------------

    #scraping primera pagina
    listaComentarios.extend(scrappingProfesor_SoloUnaPag(url,1))
    #scraping a las paginas siguientes
    if 1 < numPags:
        for i in range(2,numPags+1):
            nuevaLista=scrappingProfesor_SoloUnaPag(url + "?pag=" + str(i),i)
            listaComentarios.extend(nuevaLista)
    return listaComentarios


def main():
    listaComentarios:List[Comentario]

    url = "https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150"
    scrappingProfesor(url)




def listaComentarios_To_JSON(nombreJSON:str,listaComentarios:List[Comentario]):
    """ Genera un archivo con los comentarios guardados  de ciertos

    Args:
        nombreJSON (str): _description_
        listaComentarios (List[Comentario]): _description_
    """

    # Convierte la lista de objetos Comentario en una lista de diccionarios
    listaComentarios_dict = [comentario.to_dict() for comentario in listaComentarios]

    # Convierte la lista de diccionarios en una cadena JSON
    listaComentarios_json = json.dumps(listaComentarios_dict, ensure_ascii=False)

    # Guarda la cadena JSON en un archivo
    with open(nombreJSON, 'w', encoding='utf8') as f:
        f.write(listaComentarios_json)


def json_To_ListaComentarios(nombreJSON:str)->List[Comentario]:
    """Convierte de un diccionario Json a la lista comentarios, recordar que un archivo json es un archivo con los comentarios de un profesor

    Args:
        nombreJSON (str): ruta/archivo.json

    Returns:
        List[Comentario]: lista con los comentarios
    """

    # Carga el archivo JSON como una lista de diccionarios
    with open(nombreJSON, 'r', encoding='utf8') as f:
        listaComentarios_dict = json.load(f)

    # Convierte la lista de diccionarios en una lista de objetos Comentario
    listaComentarios = [Comentario.from_dict(comentario_dict) for comentario_dict in listaComentarios_dict]
    return listaComentarios


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



#main()
def main2():
    listaComentarios:List[Comentario]
    url = "https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150"
    nombreJSON="comen.json"

    profes,links= ExtraerNombres_links_profes("profesores.txt")

    url=links[3]
    nombreProfe=profes[3]

    print(url)

    #crear_base_datos_y_tabla()



    # scraping
    #listaComentarios=scrappingProfesor(url)

    #listaComentarios_To_JSON(nombreJSON,listaComentarios)

    recuperado=json_To_ListaComentarios(nombreJSON)

    #print(listaComentarios[0].comments)
    print(recuperado[0].comments)

    print(len(recuperado))

    #introducir_profesor(nombreProfe)




main2()
