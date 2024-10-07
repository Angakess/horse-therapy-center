import string
from flask import render_template,request, url_for, redirect
from core import user
from flask import Blueprint

from core.user.users import User
#from src.web.handlers.auth import login_required


bprint = Blueprint("users", __name__, url_prefix="/usuarios")

@bprint.get("/")
#@login_required
#@check("user_index")
def index():
    users = user.list_users()
    query = request.args.get('query', '')
    query = query.translate(str.maketrans('', '', string.punctuation))


    if query:
        users = [
            user for user in users if (
               query.lower() in user.email.lower() or
                (user.enabled and query.lower() in ['activo', 'sí']) or
                (not user.enabled and query.lower() in ['desactivado', 'no']) or
                (user.role and query.lower() in user.role.name.lower())
                )
        ]

    return render_template("auth/users.html", users=users, query=query)


@bprint.post("/activar_usuario")
def activar_usuario():
    chosen_id = request.form['id']
    query = request.form['query'] 
    user = User.query.get(chosen_id) 
    if user:
        user.activate_user()  


    return redirect(url_for('auth/users.index', query=query))