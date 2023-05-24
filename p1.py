import requests
from bs4 import BeautifulSoup

# Realizar una solicitud HTTP a la página
respuesta = requests.get('https://www.misprofesores.com/profesores/Mario-Mapy-el-Gay_162216')

# Crear un objeto BeautifulSoup con el contenido HTML de la página
sopa = BeautifulSoup(respuesta.content, 'html.parser')

# Seleccionar el elemento 'ul' con la clase "pagination"
ul = sopa.select_one('ul.pagination')

# Seleccionar todos los elementos 'li' dentro del elemento 'ul'
elementos_li = ul.select('li')

# Imprimir el número de elementos 'li'
print(len(elementos_li))
