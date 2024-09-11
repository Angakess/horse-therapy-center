from flask import Flask
from flask import render_template
from src.web.helpers import handler
from flask import request

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__)
    @app.route("/")
    def home():
        return "Bueeeenas"

    # Manejo del error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404
    
    # Error handlers
    app.register_error_handler(404, handler.not_found_error)

    return app