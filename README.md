
```yaml
Nombre Alumno: Barrera Peña Víctor Miguel
Titulo: Proyecto final análisis de texto
subtitulo:  Analisis los sentimientos comentarios profesores (misprofesores.com)
nombre de programa: Analizador misProfesores
Fecha de publicación: 08/05/2023
```

# Objetivo

El propósito es desarrollar un analizador de textos sofisticado que pueda discernir si un comentario es positivo, negativo o engañoso. Este instrumento deberá ser capaz de seleccionar a los profesores mejor calificados, basándose en los comentarios realizados en relación a una asignatura específica, con el fin de facilitar el proceso de inscripción. Este sistema de evaluación permitirá que los estudiantes tomen decisiones más informadas sobre qué profesores elegir, y ayudará a asegurar la calidad educativa y la satisfacción del estudiante.

# Introducción

La emergencia de la inteligencia artificial y del procesamiento del lenguaje natural (PLN) ha cambiado radicalmente la forma en que se procesa y se analiza la información textual. BERT (Bidirectional Encoder Representations from Transformers) es uno de los modelos que ha probado su eficiencia en variadas tareas de PLN, incluyendo el análisis de sentimientos y la detección de comentarios falsos.

Mi intención es desarrollar un analizador de texto que utilice BERT para discernir si los comentarios relacionados con la evaluación de profesores son positivos, negativos o engañosos. Este sistema será una herramienta útil para los estudiantes, ayudándoles a tomar decisiones informadas al inscribirse en cursos, eligiendo a los profesores mejor calificados.

Sin embargo, debo enfatizar que el camino hacia la realización de este proyecto está lleno de desafíos. Lograr una interpretación precisa de los sentimientos y detectar comentarios falsos exige un ajuste meticuloso del modelo y un entrenamiento riguroso.

# Desarrollo

## Construcción del programa

1. **Extractor de comentarios:** Este programa realiza *scraping* en la página misprofesores.com utilizando la biblioteca **Beautiful Soup**, almacenando los comentarios en archivos JSON individuales por cada profesor. De esta manera, se guarda cada comentario de los docentes de forma independiente.

2. **Almacenamiento en una base de datos adicional:** Obtener todos los datos de todos los profesores simultáneamente resulta impráctico, ya que cada docente cuenta con múltiples páginas de comentarios. Por lo tanto, se implementa una especie de caché que indica cuándo se recuperaron por última vez los comentarios de cada profesor.

3. **Creación de un archivo de datos para el entrenamiento:** Se genera un archivo de datos con el objetivo de entrenar el modelo de datos BERT.

4. **Entrenamiento del modelo BERT:** Utilizando los datos previamente obtenidos y organizados, se procede a entrenar el modelo BERT.

5. **Prueba del modelo** con datos diferentes a los utilizados durante el entrenamiento, con el fin de evaluar su comportamiento.

6. **Elaboración de estadísticas y métricas:** Para verificar su eficacia, se realizan estadísticas y métricas, y se elabora un informe en base a ello. Esto se lleva a cabo utilizando un conjunto de prueba con posibles respuestas, las cuales difieren de las respuestas utilizadas durante el entrenamiento del modelo.

# Diario de viaje (resolviendo el problema)

## Extracción de datos de la página web (lista de profesores) mediante técnicas de scraping

```yaml
pagina: https://www.misprofesores.com/escuelas/Facultad-de-Ingenieria_1511
```

Se detectó un problema relacionado con una etiqueta u otro aspecto al intentar obtener la información a través de técnicas de scraping. Sin embargo, al utilizar un navegador, se observó que este corrigió el error debido a la flexibilidad de HTML y JavaScript. La opción más obvia y exitosa fue realizar el scraping directamente desde el navegador, aprovechando el motor de renderizado HTML y JavaScript que solucionó los errores.

La solución consistió en utilizar la consola del navegador para llevar a cabo el scraping. Los datos se obtuvieron utilizando el método `document.getElementById`, y la salida de la consola se redirigió a un archivo de texto que se descargó en el navegador una vez que se completó la extracción de datos de los profesores.

```mermaid
graph TD;
  	misProfesores.com -->navegador;
    navegador--> consola;
    consola--> profesores.txt; 
```

El siguiente código se utiliza para realizar dicha extracción:

```js
console.save = function(data, filename) {
  if (!data) {
    console.error('No hay datos para guardar en el archivo.');
    return;
  }

  if (!filename) {
    filename = 'console.log';
  }

  if (typeof data === 'object') {
    data = JSON.stringify(data, undefined, 2);
  }

  var blob = new Blob([data], { type: 'text/plain' });
  var url = URL.createObjectURL(blob);

  var a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
};

// Variable para almacenar la salida de la consola
var salida = '';

document.querySelectorAll('table td.visible-xs').forEach(function(celda) {
  // Verificar si la celda contiene un enlace con un atributo href
  var enlace = celda.querySelector('a');
  if (enlace && enlace.hasAttribute('href')) {
    // Obtener el href y el texto "inherit" de la celda
    var href = enlace.getAttribute('href');
    var texto = celda.textContent.trim();

    // Realizar alguna operación con el href y el texto
    salida += 'href: ' + href + '\n';
    salida += 'Texto: ' + texto + '\n';
  }
});

// Guardar la salida en un archivo
console.save(salida, 'profesores.txt');
```

El programa debe ejecutarse en la página principal de misprofesores.com para una universidad específica. En el caso de tu universidad, la página principal es:

```
https://www.misprofesores.com/escuelas/Facultad-de-Ingenieria_1511
```

![Imagen principal de misprofesores.com para la facultad de ingeniería](./assets/image-20230529115914119.png)

El número en **rojo** que indica la cantidad de profesores debe tenerse en cuenta, ya que en la configuración inicial (la primera vez que ejecutes el programa), se te pedirá ese dato: 2036.

## ¿De qué tamaño es el conjunto? 

Para comprobar que la extracción sea correcta y también para saber de cuantos elementos es el conjunto de entrenamiento es necesario tener el número de cometarios

Por lo que había comentado de una etiqueta mal hecha realice una extracción directamente del navegador de la siguiente página

```yaml
pagina: https://www.misprofesores.com/escuelas/Facultad-de-Ingenieria_1511
```

con el siguiente script

```js
// Seleccionar todos los elementos <td> en la quinta posición (donde está el valor "0")
var tdElements = document.querySelectorAll('tr.odd td:nth-child(5)');

// Iniciar una variable para la suma
var suma = 0;

// Iterar a través de todos los elementos <td>
for (var i = 0; i < tdElements.length; i++) {
    // Obtener el valor de texto del elemento <td> y convertirlo a un número
    var valor = parseInt(tdElements[i].textContent);
  
    // Añadir el valor a la suma
    suma += valor;
}

// Mostrar la suma en la consola
console.log("La suma de todos los valores es: " + suma);
```

Ejecución:

```
La suma de todos los valores es: 11781
```

El conjunto es pequeño (11,781) , ya que con el conjunto de enteramiento con los que he observado que entrenan superan fácilmente los 40,000. Sin embargo hay que tener algo muy presente, puede que algunos comentarios están o estarán en **en revisión**, por lo cual se descartan y como resultado el conjunto total de comentarios puede ser menor. 

## Extracción de  los comentarios de cada profesor

A partir del documento `profesores.txt` que tiene la siguiente estructura

```yaml
href: https://www.misprofesores.com/profesores/Omar-Abrego-Blancas_161282
Texto: Abrego Blancas, OmarDIE
href: https://www.misprofesores.com/profesores/Omar-Edsiel-Abrego-Blancas_161304
Texto: Abrego Blancas, Omar EdsielFacultad de ingeniería
href: https://www.misprofesores.com/profesores/Anays-Acevedo-Barrera_150151
Texto: Acevedo Barrera, AnaysFacultad de Ingeniería
href: https://www.misprofesores.com/profesores/Guiomar-Acevedo-Lopez_78442
Texto: Acevedo Lopez, GuiomarFacultad de ingeniería
href: https://www.misprofesores.com/profesores/HERMINIO-ACEVEDO-VALLE_55012
Texto: ACEVEDO VALLE, HERMINIOFacultad de Ingeniería UNAM
...
```

Del archivo de `profesores.txt` hay que recuperar el link y el nombre del profesor y hay que colocarlo en una lista de `links` y otra de `textos` se logró con la siguiente código:

```python
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
```

## No se puede  realizar de todas las extracciones  una tras otra

Siendo una página web  y un servidor que no es tan potente al realizar 11,000, y 239 profesores, al menos tendría que realizar +400 peticiones, si se hace una tras otra me van a bloquear o puede que tirar el sitio, por tanto lo haré de manera más discreta montado en un servidor que esporádicamente hará las peticiones teniendo un tiempo aleatorio  (24 horas del día).



## Archivo de configuración

Para saber que  

## Funcionamiento del programa

```mermaid
graph TD;
A[Inicio programa] -->|*b1| B;
B{existe  configuracion?} -->|no| C([Crea la configuracion])
B--> H[*b2]
	


subgraph crear Configuracion
	C--> D[cuenta el numero de json de profesores]
	D--> E{existe la base de datos}
	E--> |si| f1[regresa *b1]
	E--> |no| F[crea la base de datos]
	F--> G[crea tabla profesores]
	G-->E
	end;

```

# Problema de las paginas web

Al tratar de obtener el número de cuantas paginas hay por cada profesor, hay un problema al obtener el número de páginas para algunos problemas, ya sea por un error de etiquetas o porque se renderiza con JavaScript y por ello se tendría que utilizar algo más potente que `Beautiful Soup` , la solución obvia fue calcular aproximadamente cuantas páginas.

**Se descartó:**

![Número de página](./assets/image-20230529123039873.png)

Entrando a cualquier profesor a la primera página de comentarios, se puede obtener el número de comentarios

![image-20230529123226902](./assets/image-20230529123226902.png)

y sabiendo que se muestran 5 comentarios por página, si tiene 6 comentarios, se tienen que hacer `scraping`  a la página 1,2, ya que hay 5 en la primera y 1 en la siguiente.

# Mejorando el scraping

No todo es posible que corra en un servidor, también es necesario que pueda continuar en automatico sin estar todo el tiempo disponible para hacer scraping, por eso utilizando en archivo de configuración guarda el último documento que fue scrapeado, la solución es suponiendo que se tiene un arreglo con todos los profesores y sus links, si el último que fue scrapeado fue el `profesor [100]` entonces se que `100` fue el último y este dato esta guardado en alchivo 

```
config.json
```

La manera que en se realiza

```mermaid
graph TD;
 id1([Inicio del programa]) -->  A[Verifica el archivo config.js]
 A--> |Recupera *I* de config.js| B[Toma el numero del ultimo profesor scraping *i*]
 B--> C[scraping al profesor *i+1*]
 C--> D{Scraping con exito?}
 D --> |no| E[ Reducir el maximo de profesores]
 D --> |si | G[Incrementa el número de archivos]
 E -->  F[Guardar config.js]
 G --> F
 F --> |incrementa *I*| B

 
```



Lo que ocasiona el anterior flujo  ocasiona que si se interrumpe en cualquier momento el flujo anterior, va regresar al ultimo estado estable, que es cuando se guardo el ultimo scraping del anterior profesor, esto funciona mientras sigas teniendo la base datos `.sql` y  los archivos `.json` que contienen los comentarios de cada profesor.

## Crear el dataset de entrenamiento 

Cuando ya se tenga completado todos los archivos `.json` se crea un archivo `.csv` que contiene la siguiente estructura:

| review                                                       | sentiment |
| ------------------------------------------------------------ | --------- |
| One of the other reviewers has mentioned that after watching just 1 Oz episode you'll be hooked. They are right, as this is exactly what happened with me.<br /><br /> | positive  |
| A wonderful little production.                               | positive  |
| I thought this was a wonderful way to spend time on a too hot summer weekend, sitting in the air conditioned theater and watching a light-hearted comedy. The plot is simplistic, but the dialogue is witty and the characters are likable (even the well bread suspected serial killer). While some may be disappointed when they realize this is not Match Point 2: Risk Addiction, | positive  |

De donde me baso para mi trabajo de investigación usaron el `Bert` en la versión ingles, además de tener comentarios en ingles, son comentarios largos y por eso acortaron el entrenamiento a 200 tokens, los resultados son posibles en 2 estados, sin embargo para este caso  son 4 estados, lo usaré con comentarios más pequeños, además el set de entrenamiento es mucho menor, y por supuesto  el modelo usado es `BETO` la versión en español de `Bert`.

## Crear dataSet de sentimientos

Para mi caso especifico he creado 4 categorias.

Tengo dos parámetros con los que puedo analizar la posibilidad 

Malo <=5 o  5< Bueno  en cuanto **Calidad general** 

Fácil <= 5 ,5< Dificil en **facilidad**

![image-20230529143512049](./assets/image-20230529143512049.png)

Entonces estoy re mapeando queda la siguiente manera

![diagrama_estados](./assets/diagrama_estados.png)

# Resultado

## Prueba 1: Acotado a 2 casos (sin drop_output)

En este caso sólo se acotó a dos casos de lo que podía distinguir el modelo entre profesor `fácil`, `díficil` para ello es necesario cambiar una  pequeña parte del código `menu3.py` que se muestra a continuación en la función ` comentarios_To_Csv`

```python
if float(commen.score_facilidad)<=5.0:
                    sentiment+= sentimientos[3] +"+" #dificil
                else:
                    sentiment+= sentimientos[2] +"+" #facil
                
                """
                if float(commen.score_general) <= 5.0:
                    sentiment+= sentimientos[1]
                else:
                    sentiment += sentimientos[0]

                """
```

**Para desactivar ** drop-out realize lo siguiente en el código de colab

```python
# EL MODELO!

class BERTSentimentClassifier(nn.Module):

  def __init__(self, n_classes):
    super(BERTSentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.linear = nn.Linear(self.bert.config.hidden_size, n_classes)

  def forward(self, input_ids, attention_mask):
    _, cls_output = self.bert(
        input_ids = input_ids,
        attention_mask = attention_mask,
        return_dict=False
    )
    #drop_output = self.drop(cls_output)
    #output = self.linear(drop_output)

    output=self.linear(cls_output)
    return output
```

**Como se observa hay líneas comentadas y se le pasa directamente a la salida sin pasar por el drop_out**

se comenta para que solo pueda  ser o `facil` o `dificil` teniendo dos posibles casos

**Tabla de pérdida:**

 Epoch  Entrenamiento  Validación
     1       0.537200    0.585725
     2       0.558802    0.579712
     3       0.564342    0.579672
     4       0.563949    0.579366
     5       0.563729    0.580076

**Tabla de precisión:** 

Epoch  Entrenamiento  Validación
     1         0.75425       0.734
     2         0.75250       0.734
     3         0.74900       0.734
     4         0.74900       0.734
     5         0.74900       0.734

Vista en tabla se observa de la siguiente manera:

![/](./assets/resultado1.png)

Si se desea repetir el experimento se tienen los archivos `prueba1.ipynb` y  `input2.csv` en la carpeta de `pruebas`



## Prueba 2: Acotado a 2 casos (con drop_output)

Es el mismo caso que el anterior sólo que aquí se descomentará  las lineas que evitaban que existiera `drop_output`, el resultado se almacenará como `prueba-2` en una capeta con su archivo de jupyter y su `csv` quedando de la siguiente manera el modelo

```python
# EL MODELO!

class BERTSentimentClassifier(nn.Module):

  def __init__(self, n_classes):
    super(BERTSentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.linear = nn.Linear(self.bert.config.hidden_size, n_classes)

  def forward(self, input_ids, attention_mask):
    _, cls_output = self.bert(
        input_ids = input_ids,
        attention_mask = attention_mask,
        return_dict=False
    )
    drop_output = self.drop(cls_output)
    output = self.linear(drop_output)

    #output=self.linear(cls_output)
    return output
```



Existe en el menú principal un modo que compara el archivo `dataSet-input.csv` que es la entrada con la que el modelo funciona

**Tabla de pérdida:**

| Epoch | Entrenamiento      | Validación         |
| ----- | ------------------ | ------------------ |
| 1     | 0.589561250180006  | 0.5809156138896943 |
| 2     | 0.5798053234815598 | 0.5806862189769745 |
| 3     | 0.5816135759353638 | 0.5801328020095825 |
| 4     | 0.5771492357552052 | 0.580109525680542  |
| 5     | 0.5737003091573715 | 0.5812571394443512 |

**Tabla de precisión:**

| Epoch | Entrenamiento | Validación |
| ----- | ------------- | ---------- |
| 1     | 74.2375       | 73.4       |
| 2     | 74.7          | 73.4       |
| 3     | 74.575        | 73.4       |
| 4     | 74.925        | 73.4       |
| 5     | 74.9          | 73.4       |

El resultado es que mejoro muy poco con respecto  a la que no tenia drop, entonces la mejora es mínima.

![resultado2](./assets/resultado2.png)

![resultado2-1](./assets/resultado2-1.png)

## Prueba 3: Acotado a 4 casos (con drop_output)

Teniendo los parámetros guardados del programa, sólo se había explotado el valor asociado a la facilidad teniendo 2 posibles opciones,**facil,dificil** , pero ahora se agregarán 2 nuevos valores de una variable, que puede ser **malo,bueno** es en calidad general, por lo cual ahora hay cuatro posibles características.

Para lograr lo anteriormente planteado es necesario crear un nuevo conjunto que incluya los nuevos valores, por ejemplo "facil-malo".

**Modificar**



En el caso de `bert` se tiene que emplear lo siguiente

```python
DATASET_PATH = '/content/drive/MyDrive/input3.csv'
NCLASSES = 4
```



Ya que el csv cambió, y el número de clases también cambió.

| Época | Pérdida de Entrenamiento | Precisión de Entrenamiento | Pérdida de Validación | Precisión de Validación |
| ----- | ------------------------ | -------------------------- | --------------------- | ----------------------- |
| 1     | 0.8956081299185753       | 0.689375                   | 0.8354219675064087    | 0.6900000000000001      |
| 2     | 0.7726683940291404       | 0.714125                   | 0.8017361276149749    | 0.705                   |
| 3     | 0.7139917816221714       | 0.734375                   | 0.7997174730300903    | 0.7065                  |
| 4     | 0.6634449841976165       | 0.7465                     | 0.8024916416406631    | 0.704                   |
| 5     | 0.6244435852468013       | 0.760625                   | 0.821673817038536     | 0.705                   |



![](./assets/resultado3-1.png)

![](./assets/resultado3-2.png)

## Prueba 4: Acotado a 4 casos (en idioma español el modelo Beto)



# Conclusión

El programa demuestra una funcionalidad excepcional al entender el concepto de cómo opera el procesamiento del lenguaje natural en las inteligencias artificiales. Este entendimiento se convierte en un gran apoyo dado el creciente interés suscitado por la aparición de modelos como GPT.

Bert es un modelo altamente versátil que puede adaptarse a múltiples propósitos, según el área en la que se desee entrenarlo. En mi caso, se utilizó para analizar sentimientos, y los resultados fueron muy satisfactorios. Al utilizar un modelo en español, los resultados fueron superiores a los obtenidos con modelos en inglés, ya que la forma de analizar los sentimientos puede variar significativamente entre diferentes idiomas. En este caso, se entrenaron modelos para detectar 2 o 4 sentimientos basándose en una respuesta, sin embargo, este modelo puede adaptarse para identificar una mayor variedad de sentimientos si se modifican los parámetros correspondientes.

# Visión futura

- El programa resulta altamente útil para entender el comportamiento de un profesor a través de sus comentarios. Esto facilita la selección de profesores en base a las evaluaciones recibidas, permitiendo a los estudiantes tomar decisiones más informadas respecto a qué cursos inscribir. En un sentido amplio, los datos podrían utilizarse para establecer un sistema de clasificación de profesores basado en las necesidades individuales de cada estudiante.
- Este analizador de sentimientos podría integrarse a plataformas como **Facebook** para obtener un análisis más profundo. Posteriormente, podría establecerse una clasificación completa del profesor basada en datos estadísticos obtenidos de todos los comentarios emitidos por los estudiantes. Además, se podría unir a un programa existente para crear configuraciones de horarios posibles, permitiendo a los estudiantes seleccionar horarios basándose en los comentarios recibidos.
- Este programa podría beneficiarse de la implementación de interfaces gráficas para mejorar la experiencia de los usuarios.
- Podría diseñarse un sistema para detectar comentarios fraudulentos cuyo objetivo sea confundir a los estudiantes con evaluaciones negativas de profesores. Para esto, solo sería necesario tomar en cuenta las fechas de baja y calcular una vecindad que se podría considerar como indicativa de actividad fraudulenta. Además, se podría recopilar información estadística sobre los profesores para conocer su tendencia generalizada.

# Referencias

- mrm8488. (2023, 29 de mayo). BETO_getting_started.ipynb. GitHub. https://colab.research.google.com/github/mrm8488/beto/blob/master/BETO_getting_started.ipynb

- Mermaid. (2023, 29 de mayo). Sintaxis de los diagramas de flujo. https://mermaid.js.org/syntax/flowchart.html

- QData. (2023, 29 de mayo). Example_4_CamemBERT.ipynb - Colaboratory. GitHub. https://colab.research.google.com/github/QData/TextAttack/blob/master/docs/2notebook/Example_4_CamemBERT.ipynb#scrollTo=koVcufVBD9uv

- CamemBERT. (2023, 29 de mayo). CamemBERT. https://camembert-model.fr/

- YouTube. (2023, 29 de mayo). [Video]. https://www.youtube.com/watch?v=IRtHuwSPaGo

- Wb-az. (2023, 29 de mayo). Transformers-Emotion-Analysis. GitHub. https://github.com/Wb-az/Transformers-Emotion-Analysis

- codificandobits. (2023, 29 de mayo). Analisis_de_sentimientos_con_BERT/BERT_analisis_sentimientos.ipynb. GitHub. https://github.com/codificandobits/Analisis_de_sentimientos_con_BERT/blob/master/BERT_analisis_sentimientos.ipynb

- Codificando Bits. (2023, 29 de mayo). Análisis de sentimientos con BERT en Python (Tutorial) [Video]. YouTube. https://www.youtube.com/watch?v=mvh7DV84mr4

- Codificando Bits. (2023, 29 de mayo). Comprensión de texto con BERT en PYTHON (Tutorial) [Video]. YouTube. https://www.youtube.com/watch?v=iPrwWtVl0LM

- Chat GPT 4.0 con Pluggins  (May 24,2023)

Das últimas 3 referencias son las que hacen entender cada parte del código
