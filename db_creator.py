import psycopg2
from flask_sqlalchemy import SQLAlchemy
import urllib
from sqlalchemy import create_engine
import pyodbc

driver = "{ODBC Driver 17 for SQL Server}"
server = "bxboysdbserver.database.windows.net"
database = "bxboysdb_portfolio"
username = "rfosha"
pwd = "Bxboys2020"

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ pwd)
cursor = conn.cursor()

#CREATE TABLES
# cursor.execute("CREATE TABLE managers (id integer IDENTITY, primaryOwner VARCHAR(100), manager VARCHAR(100));")
# print("Finished creating managers table")

# cursor.execute("CREATE TABLE arrivals (id integer IDENTITY, manager_name VARCHAR(100), day_in VARCHAR(100),"
#                "time_in VARCHAR(100), day_out VARCHAR(100), time_out VARCHAR(100));")
# print("Finished arrivals creating table")
#
# cursor.execute("CREATE TABLE bets (id integer IDENTITY, manager_name_1 VARCHAR(100), manager_name_2 VARCHAR(100),"
#                "bet VARCHAR(100), amount FLOAT, manager_name_1_signed VARCHAR(100), manager_name_2_signed VARCHAR(100));")
# print("Finished bets creating table")
#
# cursor.execute("CREATE TABLE fp_pot (id integer IDENTITY, pot FLOAT);")
# print("Finished pot creating table")
# #
# cursor.execute("CREATE TABLE fp_totals (id integer IDENTITY, manager_name VARCHAR(100), week1 FLOAT,"
#                "week2 FLOAT, week3 FLOAT, week4 FLOAT, week5 FLOAT, week6 FLOAT, week7 FLOAT, week8 FLOAT, week9 FLOAT,"
#                "week10 FLOAT, week11 FLOAT, week12 FLOAT, week13 FLOAT, week14 FLOAT, week15 FLOAT, week16 FLOAT,"
#                "amount_owed FLOAT);")
# print("Finished fp_totals creating table")
#
# cursor.execute("CREATE TABLE fp_transaction (id integer IDENTITY, manager_name VARCHAR(100), season INTEGER,"
#                "week VARCHAR(100), payout_penalty VARCHAR(100), transaction_value FLOAT, transaction_type VARCHAR(100), "
#                "transaction_description VARCHAR(5000));")
# print("Finished creating fp_transaction table")
#
# cursor.execute("CREATE TABLE fp_week_end (id integer IDENTITY, ending_balance VARCHAR(100), week1 FLOAT,"
#                "week2 FLOAT, week3 FLOAT, week4 FLOAT, week5 FLOAT, week6 FLOAT, week7 FLOAT, week8 FLOAT, week9 FLOAT,"
#                "week10 FLOAT, week11 FLOAT, week12 FLOAT, week13 FLOAT, week14 FLOAT, week15 FLOAT, week16 FLOAT,"
#                "placeholder FLOAT);")
# print("Finished creating fp_week_end table")
# #
# cursor.execute("CREATE TABLE fp_week_start (id integer IDENTITY, starting_balance VARCHAR(100), week1 FLOAT,"
#                "week2 FLOAT, week3 FLOAT, week4 FLOAT, week5 FLOAT, week6 FLOAT, week7 FLOAT, week8 FLOAT, week9 FLOAT,"
#                "week10 FLOAT, week11 FLOAT, week12 FLOAT, week13 FLOAT, week14 FLOAT, week15 FLOAT, week16 FLOAT,"
#                "placeholder FLOAT);")
# print("Finished creating fp_week_end table")
#
# cursor.execute("CREATE TABLE proposals (id integer IDENTITY, proposal_name VARCHAR(100), proposal_manager VARCHAR(100),"
#                "proposal_text VARCHAR(5000), proposal_season VARCHAR(100), proposal_status VARCHAR(100));")
# print("Finished proposals creating table")
#
# cursor.execute("CREATE TABLE requests (id integer IDENTITY, request_name VARCHAR(100), request_manager VARCHAR(100),"
#                "request_text VARCHAR(5000), request_status VARCHAR(100));")
# print("Finished creating requests table")
#
# cursor.execute("CREATE TABLE users (id integer IDENTITY, email VARCHAR(100), user_name VARCHAR(100),"
#                "user_password VARCHAR(100));")
# print("Finished user creating table")
#
# cursor.execute("CREATE TABLE side_bets (id integer IDENTITY, manager_name1 VARCHAR(100), manager_name2 VARCHAR(100),"
#                "bet_desc VARCHAR(5000), bet_amount VARCHAR(100), manager1_approval VARCHAR(100), "
#                "manager2_approval VARCHAR(100), season VARCHAR(100), bet_outcome VARCHAR(100));")
# print("Finished creating side_bets table")

#ADDING DATA
# sql = "INSERT INTO fp_week_start (starting_balance, week1, week2, week3, week4, week5, week6, week7, week8, week9, " \
#       "week10, week11, week12, week13, week14, week15, week16, placeholder) " \
#       "VALUES ('Starting Blance', 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00);"
# cursor.execute(sql)
#
# sql = "INSERT INTO fp_week_end (ending_balance, week1, week2, week3, week4, week5, week6, week7, week8, week9, " \
#       "week10, week11, week12, week13, week14, week15, week16, placeholder) " \
#       "VALUES ('Ending Blance', 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00);"
# cursor.execute(sql)
#
# sql = "INSERT INTO fp_pot (pot) " \
#       "VALUES (100.00);"
# cursor.execute(sql)
#
# managers = ['Max', 'Beasley', 'Nate', 'Chris', 'Scott', 'Ben', 'DJ', 'Gach', 'Gwinn', 'Ryan']
#
# for manager in managers:
#     sql = "INSERT INTO arrivals (manager_name, day_in, time_in, day_out, time_out) " \
#           "VALUES ('{}', 'Friday', '9:00', 'Sunday', '10:00');".format(manager)
#     cursor.execute(sql)
# print("Finished inserting starting records into arrivals table")
#
# for manager in managers:
#     sql = "INSERT INTO fp_totals (manager_name, week1, week2, week3, week4, week5, week6, week7, week8, week9, " \
#           "week10, week11, week12, week13, week14, week15, week16, amount_owed) " \
#           "VALUES ('{}', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);".format(manager)
#     cursor.execute(sql)
# print("Finished inserting starting records into fp_totals table")
#

###QUERIES TO VALIDATE CERTAIN LOADS:
# cursor.execute("SELECT * FROM arrivals;")
# records = cursor.fetchall()
# for row in records:
#     print(row)
#
# cursor.execute("SELECT * FROM users;")
# records = cursor.fetchall()
# for row in records:
#     print(row)

# cursor.execute("SELECT * FROM managers;")
# records = cursor.fetchall()
# for row in records:
#     print(row)


#COMMIT AND CLOSE
conn.commit()
cursor.close()
conn.close()


