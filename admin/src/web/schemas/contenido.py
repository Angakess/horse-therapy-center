from marshmallow import Schema, fields, post_load
from datetime import datetime


class ContenidoSchema(Schema):
    id = fields.Int(dump_only=True)
    autor = fields.Str(dump_only=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    contenido = fields.Str(required=True)
    fecha_de_creacion = fields.DateTime(dump_only=True)
    estado = fields.Str(validate=lambda x: x in ["Publicado"])

contenido_schema = ContenidoSchema()
contenidos_schema = ContenidoSchema(many=True)