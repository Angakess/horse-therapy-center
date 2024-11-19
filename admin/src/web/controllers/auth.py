from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import session
from . import check_user
from web.helpers.auth import get_google_provider_cfg
from web.oauth import oauth
from core.user import create_user
import requests
import json

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    params = request.form

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


@bp.get("/register")
def register():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = oauth.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@bp.get("/register/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = oauth.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    try:
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(oauth.google_client_id, oauth.google_client_secret),
        )

        oauth.client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = oauth.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["given_name"]
        else:
            flash("User email not available or not verified by Google.", "error")
            return redirect("/")
        try:
            create_user(email=users_email, alias=users_name, password=None, role_id=5)
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/")

    flash(
        "Operación exitosa, la sesión se encuentra pendiente para ser aceptada por un administrador",
        "success",
    )
    return redirect("/")
