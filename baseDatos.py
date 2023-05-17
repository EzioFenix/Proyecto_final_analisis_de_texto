import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta

def crear_base_datos_y_tabla():
    try:
        conexion = sqlite3.connect('registro.db')
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaActualizacion (
                nombreProfesor TEXT,
                fecha TEXT
            );
        ''')

        cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='diaActualizacion';
        ''')

        result = cursor.fetchone()

        if result:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_nombreProfesor ON diaActualizacion (nombreProfesor);
            ''')

        conexion.commit()
        conexion.close()
    except Error as e:
        print(e)

def actualizar_fecha_profesor(nombreProfesor):
    try:
        conexion = sqlite3.connect('registro.db')
        cursor = conexion.cursor()

        # Obtén la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Actualiza la fecha para el profesor dado
        cursor.execute('''
            UPDATE diaActualizacion
            SET fecha = ?
            WHERE nombreProfesor = ?;
        ''', (fecha_actual, nombreProfesor))

        conexion.commit()
        conexion.close()
    except Error as e:
        print(e)

def calcular_dias_diferencia(nombreProfesor):
    try:
        conexion = sqlite3.connect('registro.db')
        cursor = conexion.cursor()

        # Obtiene la fecha actual para el profesor dado
        cursor.execute('''
            SELECT fecha FROM diaActualizacion
            WHERE nombreProfesor = ?;
        ''', (nombreProfesor,))

        fecha_profesor = cursor.fetchone()
        if fecha_profesor is None:
            return None

        fecha_profesor = datetime.strptime(fecha_profesor[0], '%Y-%m-%d')
        fecha_actual = datetime.now()

        # Calcula la diferencia en días
        diferencia = (fecha_actual - fecha_profesor).days

        conexion.close()

        return diferencia
    except Error as e:
        print(e)

def introducir_profesor(nombreProfesor):
    try:
        conexion = sqlite3.connect('registro.db')
        cursor = conexion.cursor()

        # Obtén la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Introduce un nuevo profesor con la fecha actual
        cursor.execute('''
            INSERT INTO diaActualizacion (nombreProfesor, fecha)
            VALUES (?, ?);
        ''', (nombreProfesor, fecha_actual))

        conexion.commit()
        conexion.close()
    except Error as e:
        print(e)

