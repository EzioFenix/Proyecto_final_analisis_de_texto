import os
import re
import time
import requests
import json
import string
from bs4 import BeautifulSoup
from typing import List

from baseDatos import *
from comentario import Comentario

class Scraping():
    def __init__(self,url:str,nombreProfesor:str,carpetaGuardadoJSON:str) -> None:
        self.listaComentarios:List[Comentario]=[]
        self.url:str=url
        self.nombreProfesor:str=nombreProfesor
        self.carpetaGuardadoJSON=carpetaGuardadoJSON
        self.numPags=0
        self.numComentarios=0
        self.nombreBaseDatos="" # Nombre para buscar en base de datos
        self.ruta_completa = "" # ruta completa donde se esta guardando el archivo


    def reemplazar_puntuacion(self,texto):
        signos_puntuacion = string.punctuation

        for signo in signos_puntuacion:
            texto = texto.replace(signo, "_")
        texto = texto.replace(" ","_")

        self.nombreBaseDatos=texto

        return texto
        

    def nombreToJSon(self):
        """Convierte el nombre de guardado del archivo a ruta completa
        ejemplo: hola ==> carpeta/hola.json
        """
        carpeta=self.carpetaGuardadoJSON
        nombreNormalizado= self.reemplazar_puntuacion(self.nombreProfesor) + ".json"
        
        self.ruta_completa=os.path.join(carpeta, nombreNormalizado)
    
    
    def scrapear(self):
        print(self.nombreProfesor)
        self.nombreToJSon() # Determinamos los nombres de base de datos y ruta
        if (self.scrappingProfesor())==True:
            self.listaComentarios_To_JSON()
            return True
        else:
            return False
        


    def calcularNumeroPags(self):
        """Calcula el numero de paginas de acuerdo con el numero de comentarios totales , son 5 comentarios por pagina
        """
        numero=self.numComentarios
        self.numPags=numero//5 +int(numero % 5 > 0)


    def scrappingProfesor_SoloUnaPag(self,url:str,numPagActual:int)->List[Comentario]:
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
                calidad_general = fila.find_all('span', class_='score')[0].text.strip()
                facilidad = fila.find_all('span', class_='score')[1].text.strip()
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

                nuevoComentario=Comentario(fecha,calidad_general,facilidad,materia,textos_unidos)
                listaComentarios.append(nuevoComentario)
                
                # comprobar  que esta recolentando data--------------
                #print("Fecha:", fecha)
                #print("Materia:", materia)
                #print("Comentario:", textos_unidos)
                #print('---')
                # comprobar  que esta recolentando data--------------
                
        else:
            print("No se encontró la tabla en la página.")

        return listaComentarios


    def scrappingProfesor(self):
        """Hace scraping a la primera página de acuerdo a un profesor

        Returns:
            List[Comentario]: Lista de comentarios del profesor de su pagina mis profesores.com
        """
        response = requests.get(self.url)


        if response.status_code == 404:
            print("La página web no existe.")
            return False

        
        # Crear el objeto BeautifulSoup con el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')



        # Buscar la tabla por su clase CSS
        # -2  es poruqe el final es una vacia en li
        #self.numPags = int(soup.find_all('li')[-2].text.strip()) #metodo con errores

        #div = soup.find('div', class_='table-toggle rating-count active', attrs={'data-table': 'rating-filter'})
        #div = soup.find('div', class_='table-toggle rating-count active', attrs={'data-table': 'rating-filter'})
    

        ul = soup.select_one('ul.pagination')
        if (ul is None):
            self.numPags=0
        else:   
            elementos_li = ul.select('li')

            self.numPags=len(elementos_li)-2
            print(self.numPags)

            
            #self.numComentarios= int(num)
            #self.calcularNumeroPags()

            # scraping a las paginas--------------------------------

            #scraping primera pagina
            #elf.numPags-=1 # Todo revisar aqui que pasa
            print(self.numPags)
            self.listaComentarios.extend(self.scrappingProfesor_SoloUnaPag(self.url,1))
            #scraping a las paginas siguientes
            if 1 < self.numPags:
                for i in range(2,self.numPags+1):
                    nuevaLista=self.scrappingProfesor_SoloUnaPag(self.url + "?pag=" + str(i),i)
                    self.listaComentarios.extend(nuevaLista)
            print("termine")
            return True



    def listaComentarios_To_JSON(self):
        """ Genera un archivo con los comentarios guardados  de ciertos

        Args:
            nombreJSON (str): _description_
            listaComentarios (List[Comentario]): _description_
        """

        # Convierte la lista de objetos Comentario en una lista de diccionarios
        listaComentarios_dict = [comentario.to_dict() for comentario in self.listaComentarios]

        # Convierte la lista de diccionarios en una cadena JSON
        listaComentarios_json = json.dumps(listaComentarios_dict, ensure_ascii=False)

        if not os.path.exists(self.ruta_completa):
            os.makedirs(os.path.dirname(self.ruta_completa), exist_ok=True)

        # Guarda la cadena JSON en un archivo
        with open(self.ruta_completa, 'w', encoding='utf8') as f:
            f.write(listaComentarios_json)
        print("guarde json")


    def json_To_ListaComentarios(self)->List[Comentario]:
        """Convierte de un diccionario Json a la lista comentarios, recordar que un archivo json es un archivo con los comentarios de un profesor

        Args:
            nombreJSON (str): ruta/archivo.json

        Returns:
            List[Comentario]: lista con los comentarios
        """

        # Carga el archivo JSON como una lista de diccionarios
        with open(self.ruta_completa , 'r', encoding='utf8') as f:
            listaComentarios_dict = json.load(f)

        # Convierte la lista de diccionarios en una lista de objetos Comentario
        listaComentarios = [Comentario.from_dict(comentario_dict) for comentario_dict in listaComentarios_dict]
        return listaComentarios
