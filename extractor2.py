import requests
from bs4 import BeautifulSoup

url = "https://www.misprofesores.com/escuelas/Facultad-de-Ingenieria_1511"

# Hacer la petición a la página web
response = requests.get(url)

# Parsear el contenido de la página con BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar todas las celdas con la clase 'visible-xs'
celdas = soup.select('table td.visible-xs')

for celda in celdas:
    # Buscar enlaces dentro de la celda
    enlace = celda.find('a')
    # Verificar si el enlace existe y si tiene el atributo 'href'
    if enlace and 'href' in enlace.attrs:
        # Obtener el href y el texto de la celda
        href = enlace['href']
        texto = celda.text.strip()

        # Hacer algo con el href y el texto (aquí solo los imprimimos)
        print('href:', href)
        print('Texto:', texto)
