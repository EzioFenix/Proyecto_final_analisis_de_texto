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

#main()

def indice():
    from bs4 import BeautifulSoup

    html = '''
    <nav style="text-align:center;">
    <ul class="pagination" style="margin-top:0px;">
        <li class="disabled">
        <a aria-label="Anterior">
            <span aria-hidden="true">«</span>
        </a>
        </li>
            <li class="active"><a "="">1</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=2" "="">2</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=3" "="">3</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=4" "="">4</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=5" "="">5</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=6" "="">6</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=7" "="">7</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=8" "="">8</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=9" "="">9</a></li>
            <li><a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=10" "="">10</a></li>
            
        <li>
        <a href="https://www.misprofesores.com/profesores/nuestro-precidente--AMLO-2018_98150?pag=2" aria-label="Siguiente">
            <span aria-hidden="true">»</span>
        </a>
        </li>
    </ul>
    </nav>
    '''

    soup = BeautifulSoup(html, 'html.parser')
    last_element = soup.find_all('li')[-2].text.strip()
    print(last_element)

def listaComentarios_To_JSON(nombreJSON:str,listaComentarios:List[Comentario]):

    # Convierte la lista de objetos Comentario en una lista de diccionarios
    listaComentarios_dict = [comentario.to_dict() for comentario in listaComentarios]

    # Convierte la lista de diccionarios en una cadena JSON
    listaComentarios_json = json.dumps(listaComentarios_dict, ensure_ascii=False)

    # Guarda la cadena JSON en un archivo
    with open(nombreJSON, 'w', encoding='utf8') as f:
        f.write(listaComentarios_json)

def json_To_ListaComentarios(nombreJSON:str):

    # Carga el archivo JSON como una lista de diccionarios
    with open(nombreJSON, 'r', encoding='utf8') as f:
        listaComentarios_dict = json.load(f)

    # Convierte la lista de diccionarios en una lista de objetos Comentario
    listaComentarios = [Comentario.from_dict(comentario_dict) for comentario_dict in listaComentarios_dict]
    return listaComentarios


def ExtraerNombres_links_profes(nombre_archivo):
    # Primero, inicializamos las listas vacías
    lista_texto = []
    lista_links = []

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

    crear_base_datos_y_tabla()



    # scraping
    #listaComentarios=scrappingProfesor(url)

    #listaComentarios_To_JSON(nombreJSON,listaComentarios)

    recuperado=json_To_ListaComentarios(nombreJSON)

    #print(listaComentarios[0].comments)
    print(recuperado[0].comments)

    print(len(recuperado))

    #introducir_profesor(nombreProfe)




main2()
