from flask import render_template,request, url_for, redirect
from sqlalchemy import asc, desc
from core import user
from flask import Blueprint
from flask import flash

from core.user.roles import Role
from core.user.users import User
from core.user import create_user, list_roles, list_users, search_users, update_user,delete_user
#from src.web.handlers.auth import login_required


bprint = Blueprint("users", __name__, url_prefix="/usuarios")

@bprint.get("/")
#@login_required
#@check("user_index")
def index():
    query = request.args.get('query',"")
    role = request.args.get('role', None)
    active = request.args.get('active', None)
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'email') 
    order = request.args.get('order', 'asc')

    #Ya funciona
    if active == "True":
        active = True
    elif active == "False":
        active = False
    else:
        active = None

    

    users = search_users(email=query, role=role, active=active, page=page,sort_by=sort_by, order=order,)

    return render_template("auth/users.html", users=users.items, pagination=users)


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

@bprint.route("/register_user", methods=["GET", "POST"])
def register_user():
    roles = list_roles()
    roles = list_roles()

    if request.method == "POST":
        email = request.form['email']
        alias = request.form['alias']
        password = request.form['password']
        role_id = request.form['role'] 

        try:
            create_user(email=email, alias=alias, password=password, role_id=role_id)
            flash("Usuario registrado exitosamente.", "success")  
            return redirect(url_for("users.index"))
        except Exception as e:
            flash(f"Error al registrar el usuario: {str(e)}", "danger")

       
    return render_template("auth/register/register_user.html", roles=roles)
