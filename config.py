from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import urllib

driver = "{ODBC Driver 17 for SQL Server}"
server = "bxboysdbserver.database.windows.net"
database = "bxboysdb_portfolio"
username = "rfosha"
password = "Bxboys2020"

params = urllib.parse.quote_plus(
    'Driver=%s;' % driver +
    'Server=tcp:%s,1433;' % server +
    'Database=%s;' % database +
    'Uid=%s;' % username +
    'Pwd={%s};' % password +
    'Encrypt=yes;' +
    'TrustServerCertificate=no;' +
    'Connection Timeout=30;')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=' + params
#postgresql://user@myhost:passwd@myhost.postgres.database.azure.com:5432/mydatabase
app.secret_key = "flask rocks!"
app.config["SESSION_PERMANENT"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import Users

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))

# # blueprint for auth routes in our app
# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)
#
# # blueprint for non-auth parts of app
# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)