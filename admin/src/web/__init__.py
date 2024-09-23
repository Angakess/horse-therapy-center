from flask import Flask
from flask import render_template
from flask import url_for
from src.web.helpers import handler
from src.web.config import config
from src.web.controllers.issues import bprint as issues_bp
from src.web.controllers.auth import bp as auth_bp
from flask_session import Session
from src.core.bcrypt import bcrypt

session = Session()

def create_app(env="development",  static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    print(app.config)

    session.init_app(app)
    bcrypt.init_app(app)
    
    @app.route("/")
    def home():
        return render_template("home.html")

    # Manejo del error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404
    
    app.register_blueprint(issues_bp)
    app.register_blueprint(auth_bp)
    
    # Error handlers
    app.register_error_handler(404, handler.not_found_error)

    return app
