import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta

class BaseDatos():

    def __init__(self,nombreArchivo:str) -> None:
        self.nombreArchivo=nombreArchivo
        self.conexion = sqlite3.connect(nombreArchivo)


    def crear_base_datos_y_tabla(self,nombreArchivo:str)->bool:
        """Crea la base de datos, la tabla y la indexiación en nombreProfesor

        Args:
            nombreArchivo (str): ejemplo base.db

        Returns:
            bool: True== exito en crear la base datos
        """
        try:
            conexion = sqlite3.connect(nombreArchivo)
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
            return True

        except Error as e:
            print(e)
            return False


    def cerrarConexion(self):
        self.conexion.close()


    def actualizar_fecha_profesor(self,nombreProfesor:str):
        """Actualiza la fecha de acuerdo al nombre del profesor en tabla con la fecha actual   

        Args:
            nombreProfesor (str): nombre del profesor en la tabla
        """
        try:
            cursor = self.conexion.cursor()

            # Obtén la fecha actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d')

            # Actualiza la fecha para el profesor dado
            cursor.execute('''
                UPDATE diaActualizacion
                SET fecha = ?
                WHERE nombreProfesor = ?;
            ''', (fecha_actual, nombreProfesor))

            self.conexion.commit()
            
        except Error as e:
            print(e)


    def calcular_dias_diferencia(self,nombreProfesor:str)->int:
        """Calcula la diferencia del dia de actualización del archivo de un profesor con respecto a la fecha actual

        Args:
            nombreProfesor (str): nombre del profesor en la base de datos que se calculara la ultima actualización

        Returns:
            int: Dias de diferencia
        """
        try:
            cursor = self.conexion.cursor()

            # Obtiene la fecha actual para el profesor dado
            cursor.execute('''
                SELECT fecha FROM diaActualizacion
                WHERE nombreProfesor = ?;
            ''', (nombreProfesor,))

            fecha_profesor = cursor.fetchone()
            if fecha_profesor is None:
                return 0

            fecha_profesor = datetime.strptime(fecha_profesor[0], '%Y-%m-%d')
            fecha_actual = datetime.now()

            # Calcula la diferencia en días
            diferencia = (fecha_actual - fecha_profesor).days
            return diferencia

        except Error as e:
            print(e)


    def introducir_profesor(self,nombreProfesor:str):
        """ Introduce un nuevo nombre de profesor a la base de datosq

        Args:
            nombreProfesor (str): _description_
        """
        try:
            cursor = self.conexion.cursor()

            # Obtén la fecha actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d')

            # Introduce un nuevo profesor con la fecha actual
            cursor.execute('''
                INSERT INTO diaActualizacion (nombreProfesor, fecha)
                VALUES (?, ?);
            ''', (nombreProfesor, fecha_actual))

            self.conexion.commit()

        except Error as e:
            print(e)

