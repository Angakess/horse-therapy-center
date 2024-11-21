import logging
from flask import Flask
from flask import render_template
from flask import url_for
from web.helpers import handler
from web.config import config
from web.controllers.issues import bprint as issues_bp
from web.controllers.auth import bp as auth_bp
from web.controllers.equipo import bprint as equipo_bp
from web.controllers.users import bprint as users_bp
from web.controllers.ecuestre import bprint as ecuestre_bp
from web.controllers.pago import bprint as pago_bp
from web.controllers.jya import bprint as jya_bp
from web.controllers.cobro import bprint as cobro_bp
from web.controllers.reporte import bprint as reporte_bp
from web.controllers.contacto import bprint as con_bp
from web.api.contacto import bprint as contacto_api
from web.controllers.contenido import bprint as contenido_bp
from web.api.contenido import bprint as contenido_api
from flask_session import Session
from core.bcrypt import bcrypt
from web.helpers.auth import is_authenticated, check_permission
from web.storage import storage
from oauthlib.oauth2 import WebApplicationClient
from web.oauth import oauth
from flask_cors import CORS

session = Session()
from core import database
from core import seeds

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    print(app.config)

    session.init_app(app)
    bcrypt.init_app(app)

    database.init_app(app)

    storage.init_app(app)

    oauth.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    # Manejo del error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html"), 404

    # Manejo del error 401
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template("error.html"), 401

    # Manejo del error 403
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html"), 403

    # Función para jinja
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)

    # Registro blueprints
    app.register_blueprint(issues_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipo_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(ecuestre_bp)
    app.register_blueprint(pago_bp)
    app.register_blueprint(jya_bp)
    app.register_blueprint(cobro_bp)
    app.register_blueprint(reporte_bp)
    app.register_blueprint(con_bp)
    app.register_blueprint(contenido_bp)
    # apis
    app.register_blueprint(contacto_api)
    app.register_blueprint(contenido_api)

    # Error handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized)
    app.register_error_handler(403, handler.forbidden)

    # Comandos personalizados
    @app.cli.command(name="reset-db")
    def reset_db():
        print("Reset command registered")
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    #Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app
