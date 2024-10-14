from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 
    
def unauthorized(e):
    kwargs = {
        "error_name": "401 Unathorized",
        "error_description": "usted no tiene acceso a esta sección",
    }
    return render_template("error.html", **kwargs), 401
