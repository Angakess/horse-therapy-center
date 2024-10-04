from flask import redirect, render_template, request, url_for
from core import equipo
from flask import Blueprint

bprint = Blueprint("equipo", __name__, url_prefix="/equipo")


@bprint.get("/")
def index():
    equipos = equipo.list_equipos()
    query = request.args.get('query','')
    order = request.args.get('order', 'asc')
    by = request.args.get('by','')

    if query:
        equipos = [
            equipo for equipo in equipos if (
                query.lower() in equipo.nombre.lower() or
                query.lower() in equipo.apellido.lower() or
                query.lower() in str(equipo.dni) or
                query.lower() in equipo.email.lower() or
                query.lower() in equipo.puesto.lower()
            )
        ]
    
    if by == 'nombre':
        equipos.sort(key=lambda x: x.nombre, reverse=order == 'asc')
    elif by == 'apellido':
        equipos.sort(key=lambda x: x.apellido, reverse=order == 'asc')
    elif by == 'fecha':
        equipos.sort(key=lambda x: x.inserted_at, reverse=order == 'asc')
    else:
        equipos.sort(key=lambda x: x.id)

    return render_template("equipo/index.html", equipos=equipos, parametro=query, order=order, by=by)

@bprint.post("/toggle-active")
def toggle_activate():
    chosen_id = request.form['id']
    query = request.form['query']   #guardo lo que haya en la barra de busqueda para no resetearla
    order = request.form['order']
    by = request.form['by']
    equipo.toggle_a(chosen_id)

    return redirect(url_for('equipo.index', query=query, order=order, by=by))
