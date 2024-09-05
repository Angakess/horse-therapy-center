from flask import Flask
from flask import render_template

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__)
    @app.route("/")
    def home():
        return "Bueeeenas"
    return app