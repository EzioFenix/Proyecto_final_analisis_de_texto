from baseDatos import BaseDatos
import json
import os

class Config():
    def __init__(self) -> None:
        self.archivo_config = "config.json"
        self.archivo_db="registro_Scraping.db"
        self.numMaxProfesores:int=0
        self.numArchivosJson:int=0
        self.estadoBase:bool=False #true 

        
    def leer_configuracion(self):
        with open(self.archivo_config, 'r') as json_file:
            data = json.load(json_file)
            self.numMaxProfesores = data.get('numMaxProfesores')
            self.numArchivosJson = data.get('numArchivosJson')
            self.estadoBase = data.get('estadoBase')


    def guardar_configuracion(self):
        data = {
            'numMaxProfesores': self.numMaxProfesores,
            'numArchivosJson': self.numArchivosJson,
            'estadoBase': self.estadoBase
        }
        with open(self.archivo_config, 'w') as json_file:
            json.dump(data, json_file, indent=4)


    def contar_carpeta_comentarios(self)->int:
        carpeta = "comentarios-porProfe"

        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print("Se ha creado la carpeta 'comentarios'.")
            return 0

        num_archivos_json = 0
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".json"):
                num_archivos_json += 1
        return num_archivos_json


    def verificar_BaseDatos(self)->bool:
        if os.path.isfile(self.archivo_config):
            return True
        else:
            return False


    def recuperarBaseDatos(self):
        pass

    def iniciarConfig(self):
        
        if os.path.isfile(self.archivo_config):
            print("El archivo config.json existe.")
            self.leer_configuracion()
        else:
            print("El archivo config.json no existe.")

            self.numMaxprofesores=int(input("¿cuantos profesores tiene la escuela a scraping?").strip())

            # contar el numero de archivos jsonComentarios´
            self.numArchivosJson=self.contar_carpeta_comentarios()

            estadoBase=self.verificar_BaseDatos()
            if (estadoBase):
                pass
            else:
                if (0<self.numArchivosJson):
                    self.recuperarBaseDatos()
                else:
                    db=BaseDatos(self.archivo_db)
                    db.crear_base_datos_y_tabla()
                    
                self.estadoBase=True


            # se guarda la configuracion
            self.guardar_configuracion()
