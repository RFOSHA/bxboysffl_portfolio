from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
##password is: rfosha
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

conn_str = 'mssql+pyodbc:///?odbc_connect=' + params
engine = create_engine(conn_str)

# engine = create_engine('sqlite:///bxboys.db', convert_unicode=True, connect_args={'check_same_thread': False})
# host = "bxboysffltestpostgres.postgres.database.azure.com"
# dbname = "postgres"
# user = "user@bxboysffltestpostgres"
# password = "42itZX!1"
# sslmode = "require"
# port = '5432'

# Construct connection string
# conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

# engine = create_engine(
#     "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=require".format(user, password, host, port, dbname))


db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)