class Comentario:
    def __init__(
        self,
        fecha: str,
        score_general:int,
        score_facilidad:int,
        materia: str,
        comments: str
        ) -> None:
        
        self.fecha = fecha
        self.score_general=score_general
        self.score_facilidad=score_facilidad
        self.materia = materia
        self.comments = comments
    
    # Este método convierte el objeto en un diccionario
    def to_dict(self):
        """Convierte a diccionario el comentario

        Returns:
            dict: diccionario creado
        """
        return {
            'fecha': self.fecha,
            'score_general':self.score_general,
            'score_facilidad':self.score_facilidad,
            'materia': self.materia,
            'comments': self.comments
        }

    # Este método estático crea un nuevo objeto Comentario a partir de un diccionario
    @staticmethod
    def from_dict(source):
        """Convierte de un diccionario a un comentario

        Args:
            source (dict): diccionario que se convertira a comentario

        Returns:
            Comentario: objeto creado a diccionario
        """
        return Comentario(
            fecha=source['fecha'],
            score_general=source['score_general'],
            score_facilidad=source['score_facilidad'],
            score_Total=source['score_Total'],
            materia=source['materia'],
            comments=source['comments']
        )