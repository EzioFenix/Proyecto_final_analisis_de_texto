
def ExtraerProfes(nombre_archivo):
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


def main(): 
    listaNombres,listaLinks=ExtraerProfes("profesores.txt")

    print(len(listaNombres))
    print(listaLinks[3])





if __name__=="__main__":
    main()