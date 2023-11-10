#COMP 3450: Karan Nurlybekov Ethan Warner
from urllib import parse
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_socketio import SocketIO


# init SQLAlchemy so we can use it later in our models

# db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # socketio = SocketIO(app)
    driver = '{ODBC Driver 18 for SQL Server}'
    server = 'acresproject.database.windows.net'
    database = 'toolfooldb'
    username = 'admin123'
    password = 'Qwerty123'
    app.config['SECRET_KEY'] = 'Qwerty123'
    params = parse.quote_plus(
        f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['BOOTSTRAP_SERVE_LOCAL'] = False
    app.config['BOOTSTRAP_LOAD_REMOTE'] = True
    app.config['BOOTSTRAP_QUERYSTRING_REVVING'] = False
    app.config['BOOTSTRAP_QUERYSTRING_REFRESHING'] = False

    # db.init_app(app)
    db = SQLAlchemy(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #

    from flask_login import UserMixin

    class user(UserMixin, db.Model):
        __tablename__ = 'users'

        account_createddate = db.Column(db.DateTime, nullable=False)
        account_login = db.Column(db.String(50), nullable=False)
        account_password = db.Column(db.String(60), nullable=False)
        accouint_lat = db.Column(db.Float, nullable=False)
        accouint_lon = db.Column(db.Float, nullable=False)
        user_fname = db.Column(db.String(50), nullable=False)
        user_lname = db.Column(db.String(50), nullable=False)
        user_birthdate = db.Column(db.String(50), nullable=True)
        user_tools = db.Column(db.Float, nullable=True)
        user_orders = db.Column(db.Float, nullable=True)
        user_id = db.Column(db.Integer, primary_key=True, nullable=False)



    # from models import employees

    @login_manager.user_loader
    def load_user(id):
        return user.query.get(int(id))

    from views import views
    from auth import auth
    from signup import signupBlueprint
    from addtool import toolprint
    # from reports import reports_bp
    from tables import tables_bp
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(signupBlueprint, url_prefix='/')
    app.register_blueprint(toolprint, url_prefix='/')
    # app.register_blueprint(reports_bp, url_prefix='/')
    app.register_blueprint(tables_bp, url_prefix='/')

    return app
