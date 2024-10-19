from flask import abort, render_template,request, session, url_for, redirect
from sqlalchemy import asc, desc
from core import user
from flask import Blueprint
from flask import flash

from core.user.roles import Role
from core.user.users import User
from core.user import create_user, list_roles, list_users, search_users, update_user,delete_user
from web.helpers.auth import check_permission, is_authenticated
#from src.web.handlers.auth import login_required


bprint = Blueprint("users", __name__, url_prefix="/usuarios")

@bprint.get("/")

def index():
    '''
        Función que muestra las tablas de usuario, permite busqueda y paginación
        Parameters: Ninguno(Depende en los parametros de la query)
        Returns: Renderiza template HTML para la lista de usuarios con paginación   
     '''
    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "users_index"):
        return abort(403)
    query = request.args.get('query',"")
    role = request.args.get('role', None)
    active = request.args.get('active', None)
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'email') 
    order = request.args.get('order', 'asc')

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
    '''Funcion que permite habilitar/deshabilitar el usuario a menos que sea System Admin'''
    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "users_activar_usuario"):
        return abort(403)
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
    ''' 
    Función que edita el usuario y agrega los parametros a un diccionario para 
    no tener que hacer validación extra en update_user
    '''

    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "users_edit_user"):
        return abort(403)
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
    '''
        Función que elimina fisicamente un usuario
        Parameters: Ninguno(Depende en los parametros de la query)
        Raise: ValueError propagado por delete_user() 
     '''
    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "users_delete_user_controller"):
        return abort(403)
    

    user_id = request.form.get("user_id")  
    try:
        delete_user(user_id) 
        flash("Usuario eliminado correctamente.", "success")  
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('users.index'))

@bprint.route("/register_user", methods=["GET", "POST"])
def register_user():
    '''
        Función que registra un nuevo usuario
        Parameters: Ninguno(Depende en los parametros de la query)
        Raise: ValueError propagado de create_user()
        Returns: Renderiza template HTML para el formulario de registro y al index si el registro es correcto  
     '''

    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "users_register_user"):
        return abort(403)

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
