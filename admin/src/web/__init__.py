from flask import Flask
from flask import render_template
from src.web.helpers import handler
from src.web.controllers.issue import issue_blueprint
from flask import request
from src.core.issue import issues

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__)
    @app.route("/")
    def home():
        return "Bueeeenas"

    @app.route("/issues/")
    def issues_index():
        return render_template("issues/index.html", issues=issues)
    
    app.register_blueprint(issue_blueprint)

    # Error handlers
    app.register_error_handler(404, handler.not_found_error)

    return app