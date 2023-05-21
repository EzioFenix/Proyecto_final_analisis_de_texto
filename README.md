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

1. **Extractor de comentarios:** Este programa realiza *scraping* a la página misprofesores.com utilizando **Beautiful Soup**, almacenando los comentarios en archivos JSON individuales por cada profesor. De esta forma, los comentarios de cada docente se guardan de manera independiente.

2. **Almacenamiento en una base de datos adicional:** Es impráctico obtener todos los datos de todos los profesores de manera simultánea, dado que cada docente cuenta con múltiples páginas de comentarios. Por ello, se guarda una especie de *cache* que indica cuándo fue la última vez que se recuperaron los comentarios de cada profesor.

3. **Creación de un archivo de datos para el entrenamiento:** Se genera un archivo de datos con el objetivo de poder entrenar el modelo de datos BERT.

4. **Entrenamiento del modelo BERT:** Con los datos previamente obtenidos y organizados, se procede a entrenar el modelo BERT.

5. **Prueba del modelo** con datos diferentes a los utilizados durante el entrenamiento, con el fin de observar su comportamiento.

6. **Elaboración de estadísticas y métricas:** Para verificar su eficacia, se realizarán estadísticas y métricas, y se elaborará un informe de ello. Esto se llevará a cabo utilizando un conjunto de prueba con posibles respuestas, que son diferentes a las respuestas con las que se entrenó el modelo.



# Resultado

## 

# Conclusión

# Visión futura

# Conclusiones
