import string
from flask import render_template,request, url_for, redirect
from core import user
from flask import Blueprint
from flask import flash

from core.user.roles import Role
from core.user.users import User
from core.user import update_user,delete_user
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

    users.sort(key=lambda x: x.id)
    return render_template("auth/users.html", users=users, query=query)


@bprint.post("/activar_usuario")
def activar_usuario():
    """
    Funcion que permite habilitar/deshabilitar el usuario a menos que sea System Admin
    """
    chosen_id = request.form['id']
    query = request.form['query']
    user = User.query.get(chosen_id)

    try:
        if user:
            if user.enabled:
                user.deactivate_user()  
            else:
                user.activate_user() 
        return redirect(url_for('users.index', query=query))
    except ValueError as e:
        flash(str(e), 'danger') 
        return redirect(url_for('users.index', query=query))
    

@bprint.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    """ Función que edita el usuario y agrega los parametros a un diccionario para ahorrar 
        validación en la funcion update_user
    """
    user = User.query.get_or_404(user_id)  
    roles = Role.query.all()  

    if request.method == "POST":
        alias = request.form.get('alias')
        role_id = request.form.get('role')

        updates = {}
        if alias:
            updates['alias'] = alias
        if role_id:
            updates['role_id'] = role_id

        update_user(user_id, **updates)

        return redirect(url_for('users.index')) 

    return render_template("auth/edit_user.html", user=user, roles=roles)

@bprint.post("/delete_user")
def delete_user_controller():
    user_id = request.form.get("user_id")  
    try:
        delete_user(user_id) 
        flash("Usuario eliminado correctamente.", "success")  
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('users.index'))

