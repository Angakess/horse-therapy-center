from flask import Flask
from flask import render_template
from flask import url_for


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__)
    @app.route("/")
    def home():
        #Cambiar por el home.html
        return render_template('layout.html')
    return app