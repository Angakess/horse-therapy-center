from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import session
from . import find_user_by_email_and_password

bp = Blueprint("auth", __name__, url_prefix= "/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = find_user_by_email_and_password(params["usermail"], params["password"])

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect("/auth/")#CONSULTAR SI LAS URLS ESTÁN BIEN PUESTAS DE ESTA MANERA
    else:
        session["user"] = user.usermail
        flash("La sesión se inició correctamente", "success")
        return redirect("/consultas/")

@bp.get("/logout")
def logout():
    pass

