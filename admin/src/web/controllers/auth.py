from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import session
from . import check_user

bp = Blueprint("auth", __name__, url_prefix= "/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.post("/authenticate")
def authenticate():
    params = request.form
    print(params["usermail"])
    print(params["password"])

    user = check_user(params["usermail"], params["password"])

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect("/auth/")
    else:
        session["user"] = user.email
        flash("La sesión se inició correctamente", "success")
        return redirect("/")

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente", "info")
    else:
        flash("No hay sesión activa", "error")
    return redirect("/")

