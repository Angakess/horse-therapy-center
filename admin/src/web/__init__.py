from flask import Flask
from flask import render_template
from flask import url_for
from web.helpers import handler
from web.config import config
from web.controllers.issues import bprint as issues_bp
from core import database
from core import seeds
from core.config import config


def create_app(env="development",  static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    print(app.config)
    
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    # Manejo del error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404
    
    app.register_blueprint(issues_bp)
    
    # Error handlers
    app.register_error_handler(404, handler.not_found_error)


    # Comandos personalizados
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
