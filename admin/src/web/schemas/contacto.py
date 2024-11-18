from marshmallow import Schema, fields, post_load
from datetime import datetime


class ConsultaSchema(Schema):
    id = fields.Int(dump_only=True)  
    nya = fields.Str(required=True)
    email = fields.Str(required=True)
    cuerpo = fields.Str(required=True)
    fecha = fields.DateTime(dump_only=True, default=datetime.now)
    fecha_resuelta = fields.DateTime(allow_none=True)
    estado = fields.Str(validate=lambda x: x in ["Pendiente", "Resuelta"])

