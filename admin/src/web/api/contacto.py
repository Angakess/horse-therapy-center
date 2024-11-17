from flask import request, jsonify
from flask import Blueprint
from core.contacto import Consulta
from core.database import db
from web.schemas.contacto import ConsultaSchema

bprint = Blueprint("contacto_api", __name__, url_prefix="/api/contacto")

@bprint.post("/messages")
def create_message():
    """Crea un nuevo mensaje de consulta y lo guarda en la base de datos."""
    consulta_schema = ConsultaSchema()
    try:
        consulta_data = consulta_schema.load(request.json)
        consulta = Consulta(**consulta_data)
        db.session.add(consulta)
        db.session.commit()
        result = consulta_schema.dump(consulta_data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


