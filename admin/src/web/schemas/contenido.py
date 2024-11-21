from marshmallow import Schema, fields, post_load
from datetime import datetime

estado_traducciones= {
        "Publicado": "published",
        "Borrador": "draft",
        "Archivado": "filed"
    }

class ContenidoSchema(Schema):
    titulo = fields.Str(required=True, data_key="title")
    copete = fields.Str(required=True, data_key="summary")
    contenido = fields.Str(required=True, data_key="content")
    fecha_de_publicacion = fields.DateTime(data_key="published_at")
    fecha_de_actualizacion = fields.DateTime(data_key="updated_at")

    #Me trae el nombre del autor, así no me da el autor completo
    author = fields.Function(lambda obj: obj.autor.alias if obj.autor else None)

    #Me trae el nombre del estado, así no me da el estado completo y rraduce el estado o deja el original si no hay traducción
    status = fields.Function(lambda obj: estado_traducciones.get(obj.estado.name) if obj.estado else "unknown")
    
contenidos_schema = ContenidoSchema(many=True)
