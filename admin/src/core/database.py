from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config(app)

    return app

def config(app):
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app

def reset():
    print("Eliminando base de datos...")
    db.drop_all()
    print("Creando base nuevamente...")
    db.create_all()
    print("Done!")