import requests
from bs4 import BeautifulSoup

url = "https://www.misprofesores.com/escuelas/Facultad-de-Ingenieria_1511"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Encuentra todas las tablas
tablas = soup.find_all('table')

print(tablas)

for tabla in tablas:
    # Encuentra todas las filas de la tabla
    filas = tabla.find_all('tr')

    # Ignora la primera fila
    filas = filas[1:]

    for fila in filas:
        # Encuentra la celda y el enlace dentro de la celda
        celda = fila.find('td', {'class': 'visible-xs'})
        
        # Si la celda existe, extrae el nombre y el enlace
        if celda is not None:
            enlace = celda.find('a')
            
            # Si el enlace existe, extrae el nombre y el enlace
            if enlace is not None:
                nombre = enlace.get_text(strip=True)
                link = enlace['href']
                
                print(f'{nombre} | {link}')
