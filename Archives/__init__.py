from flask import Flask, render_template, url_for, request, redirect, flash
import sqlite3
import sys
from dbconnect import connection
import pandas as pd
from config import app
from db_setup import init_db, db_session
from forms import ProposalForm, ArrivalForm, FPTransactionForm
from flask import flash, render_template, request, redirect
from models import Proposal, Users, FP_Totals, Arrivals, FP_Pot, FP_Transactions, FP_Week_End, FP_Week_Start
from saveData import save_proposal, save_arrival
from tables import Amendment_Table, FP_Total_Table, Arrivals_Table, FP_Pot_Table, FP_Transaction_Table, FP_Week_End_Table, FP_Week_Start_Table
from flask_login import LoginManager
#from updateDatabaseForTesting import resetQADate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

init_db()

# login_manager = flask_login.LoginManager()
#
# login_manager.init_app(app)

# app = Flask(__name__)
# app.secret_key = 'adsfh89eadfa'

@app.route('/', methods=["GET", "POST"])
def login():
    return render_template('login_template.html')
# def login_page():
    # if request.method == "POST":
    #
    #     #Old query using MySQL
    #     # try:
    #     #     cursor, conn = connection()
    #     #
    #     # except Exception as e:
    #     #     return (str(e))
    #
    #     # sql = open("login_sql.sql", "r").read().replace('{}', attempted_username)
    #     # cursor.execute(sql)
    #     # result = cursor.fetchall()
    #     # conn.close()
    #
    #     # if len(result) == 0:
    #     #     flash("Invalid credentials. Try Again.")
    #     #     return render_template("login2.html")
    #     #
    #     # else:
    #     #     if attempted_username == result[0][1] and attempted_password == result[0][2]:
    #     #         return redirect(url_for('homepage'))
    #     #
    #     #     else:
    #     #         flash("Invalid credentials. Try Again.")
    #     #         return render_template("login2.html")
    #
    #     attempted_username = request.form['username']
    #     attempted_password = request.form['password']
    #
    #     try:
    #         qry = db_session.query(Users).filter(
    #             Users.user_name==attempted_username)
    #         user = qry.first()
    #         print(user.user_name)
    #         if user.user_password == attempted_password:
    #             return redirect(url_for('homepage'))
    #         else:
    #             flash("Invalid credentials. Try Again.")
    #             return render_template("login2.html")
    #
    #     except Exception as e:
    #         flash("Invalid credentials. Try Again.")
    #         return render_template("login2.html")
    #
    # return render_template("login2.html")

@app.route('/bylaws/', methods = ['GET', 'POST'])
@login_required
def bylaws():
    # if request.method == "POST":
    #     #try:
    #     cursor, conn = connection()
    #
    #     #except Exception as e:
    #     #    return (str(e))
    #
    #     amendmentName = request.form['amendmentTitle']
    #     managerName = request.form['managerName']
    #     amendment = request.form['amendment']
    #
    #     sql = open("insertAmendment.sql", "r").read().replace('amendment_Name', amendmentName)
    #     sql = sql.replace('manager_Name', managerName)
    #     sql = sql.replace('propasal_text', amendment)
    #     cursor.execute(sql)
    #     conn.commit()
    #     conn.close()
    #     return redirect(url_for('bylaws'))
    #
    # else:
    #
    #     cursor, conn = connection()
    #     sql = open("proposals.sql", "r").read()
    #     df = pd.read_sql(sql, conn)
    #     conn.close()
    #
    #     df = df.rename(columns={'amendmentName': 'Amendment Name', 'managerName': 'Manager Name', 'proposal': 'Proposal', 'status': 'Status'})
    #     data = df.values.tolist()

    return render_template("bylaws.html")

@app.route('/homepage/', methods=["GET","POST"])
@login_required
def homepage():
    return render_template("index.html")

@app.route('/freeparking/', methods=["GET","POST"])
@login_required
def freeparking():

    # resetQADate()
    # print('QA Data Reset')

    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',
             'Week 9', 'Week 10', 'Week 11', 'Week 12', 'Week 13', 'Week14', 'Week 15', 'Week 16']

    # weeks = ['Week 1']

    #gets data from the transaction input form
    if request.method == 'POST':
        manager_name = request.form['manager_name']
        season = request.form['season']
        tx_week = request.form['week']
        payout_penalty = request.form['payout_penalty']
        transaction_value = request.form['transaction_value']
        transaction_value = float(transaction_value)
        transaction_type = request.form['transaction_type']
        transaction_description = request.form['transaction_description']

        #builds the transaction object to be saved
        fp_transactions = FP_Transactions(manager_name, season, tx_week, payout_penalty, transaction_value,
                                          transaction_type, transaction_description)

        #adds the collected data for the transaction to database; adds record to fp_transaction
        db_session.add(fp_transactions)
        db_session.commit()

        #parses the week input to get the week number converted to an integer
        # length = len(week)
        # week_num = int(week[4:length])


        #code block to update manager totals
        conn = sqlite3.connect("bxboys.db")
        c = conn.cursor()
        sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(tx_week.lower().replace(" ", ""),
                                                                          manager_name)
        week_n_manager_object = c.execute(sql)
        for row in week_n_manager_object:
            week_n_manager_value = row[0]
            print("Manager (" + str(manager_name + ") STARTING VALUE:"))
            print(week_n_manager_value)

        c = conn.cursor()
        sql = "SELECT {} FROM fp_week_start".format(tx_week.lower().replace(" ", ""))
        week_n_starting_object = c.execute(sql)
        for row in week_n_starting_object:
            week_n_starting_value_man = row[0]
            print(str(tx_week) + "STARTING VALUE:")
            print(week_n_starting_value_man)
        c.close()

        if transaction_type == 'Dollar Amount' and payout_penalty == 'Payout':
            week_n_manager_update = week_n_manager_value - transaction_value
        elif transaction_type == 'Dollar Amount' and payout_penalty == 'Penalty':
            week_n_manager_update = week_n_manager_value + transaction_value
        elif transaction_type == 'Percentage of Pot' and payout_penalty == 'Payout':
            week_n_manager_update = week_n_manager_value - ((transaction_value / 100) * week_n_starting_value_man)
        else:
            week_n_manager_update = week_n_manager_value + ((transaction_value / 100) * week_n_starting_value_man)

        c = conn.cursor()
        sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(tx_week.lower().replace(" ", ""),
                                                                              week_n_manager_update, manager_name)
        print("SQL: ")
        print(sql)
        c.execute(sql)
        conn.commit()

        for week in weeks:
            c = conn.cursor()
            sql = "SELECT {} FROM fp_week_start".format(week.lower().replace(" ", ""))
            week_n_starting_object = c.execute(sql)
            for row in week_n_starting_object:
                week_n_starting_value = row[0]
                print(str(week) + " STARTING VALUE:")
                print(week_n_starting_value)
            c.close()

            c = conn.cursor()
            sql = "SELECT {} FROM fp_totals".format(week.lower().replace(" ", ""))
            transactions_for_week_n_obj = c.execute(sql)

            week_total = 0

            for transaction in transactions_for_week_n_obj:
                print("TRANSACTION:")
                print(transaction[0])
                week_total = week_total + transaction[0]
                print(week)

            week_total = week_n_starting_value + week_total

            length = len(week)
            week_num = int(week[4:length])
            print("WEEK NUMBER " + str(week_num))

            print("UPDATING WEEK_END_DATA:")
            week_end = 'Week ' + str(week_num)
            c = conn.cursor()
            sql = "UPDATE fp_week_end SET {} = '{}'".format(week_end.lower().replace(" ", ""),
                                                                                  week_total)
            print(sql)
            c.execute(sql)
            conn.commit()
            print("WEEK ENDING VALUE UPDATED")

            length = len(week)
            week_num_plus_one = int(week[4:length]) + 1

            if week_num_plus_one == 17:
                break
            else:
                print("UPDATING START VALUES: ")
                week_plus_one = 'Week ' + str(week_num_plus_one)
                c = conn.cursor()
                sql = "UPDATE fp_week_start SET {} = '{}'".format(week_plus_one.lower().replace(" ", ""),
                                                                                      week_total)
                print(sql)
                c.execute(sql)
                conn.commit()

        c = conn.cursor()
        sql = "SELECT * FROM fp_totals"
        print("SQL: ")
        print(sql)
        manager_totals_obj = c.execute(sql)

        for manager_item in manager_totals_obj:
            print('MANAGER:')
            print(manager_item)
            i = 2
            total = 0
            while i < 18:
                total = total + manager_item[i]
                i += 1

            c = conn.cursor()
            sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(total, manager_item[1])
            print("SQL: ")
            print(sql)
            c.execute(sql)
            conn.commit()

        c = conn.cursor()
        sql = "SELECT week16 FROM fp_week_end"
        final_end_value_obj = c.execute(sql)

        for value in final_end_value_obj:
            final_end_value = value[0]
            print(final_end_value)
        sql = "UPDATE fp_week_end SET placeholder = {}".format(final_end_value)
        c.execute(sql)
        conn.commit()
        sql = "UPDATE fp_week_start SET placeholder = {}".format(final_end_value)
        c.execute(sql)
        conn.commit()
        sql = "UPDATE fp_pot SET pot = {}".format(final_end_value)
        c.execute(sql)
        conn.commit()

            # while week_num <= 16:
            #     week_end = 'Week ' + str(week_num)
            #     c = conn.cursor()
            #     sql = "UPDATE fp_week_end SET {} = '{}'".format(week_end.lower().replace(" ", ""),
            #                                                                           week_total)
            #     print(sql)
            #     c.execute(sql)
            #     conn.commit()
            #     week_num = week_num + 1
            #     print(week_num)
            #     print("WEEK ENDING VALUE UPDATED")
            #
            #
            # length = len(tx_week)
            # week_num_plus_one = int(tx_week[4:length]) + 1
            #
            # print("UPDATING START VALUES: ")
            # while week_num_plus_one <= 16:
            #     week_plus_one = 'Week ' + str(week_num_plus_one)
            #     c = conn.cursor()
            #     sql = "UPDATE fp_week_start SET {} = '{}'".format(week_plus_one.lower().replace(" ", ""),
            #                                                                           week_total)
            #     print(sql)
            #     c.execute(sql)
            #     conn.commit()
            #     week_num_plus_one = week_num_plus_one + 1




        # for week in weeks:
        #     print("WEEK:")
        #     print(week)
        #
        #     c = conn.cursor()
        #     sql = "SELECT * FROM fp_transaction WHERE week = '{}' ORDER BY id".format(week)
        #     transactions_for_week_n_obj = c.execute(sql)
        #
        #     c = conn.cursor()
        #     sql = "SELECT {} FROM fp_week_start".format(week.lower().replace(" ", ""))
        #     week_n_starting_object = c.execute(sql)
        #     for row in week_n_starting_object:
        #         week_n_starting_value = row[0]
        #         print(str(week) + " STARTING VALUE:")
        #         print(week_n_starting_value)
        #     c.close()
        #
        #     for transaction in transactions_for_week_n_obj:
        #         print("TRANSACTION:")
        #         print(transaction)
        #         tx_type = transaction[4]
        #         amount = transaction[5]
        #         unit = transaction[6]
        #         print(tx_type, amount, unit)
        #
        #         if unit == 'Dollar Amount' and tx_type == 'Payout':
        #             week_n_ending_value = week_n_starting_value - amount
        #         elif unit == 'Dollar Amount' and tx_type == 'Penalty':
        #             week_n_ending_value = week_n_starting_value + amount
        #         elif unit == 'Percentage of Pot' and tx_type == 'Payout':
        #             week_n_ending_value = week_n_starting_value - ((amount / 100) * week_n_starting_value)
        #         else:
        #             week_n_ending_value = week_n_starting_value + ((amount / 100) * week_n_starting_value)
        #
        #         length = len(tx_week)
        #         week_num = int(tx_week[4:length])
        #         print("WEEK NUMBER " + str(week_num))
        #
        #         print("UPDATING WEEK_END_DATA:")
        #         while week_num <= 16:
        #             week_end = 'Week ' + str(week_num)
        #             c = conn.cursor()
        #             sql = "UPDATE fp_week_end SET {} = '{}'".format(week_end.lower().replace(" ", ""),
        #                                                                                   week_n_ending_value)
        #             print(sql)
        #             c.execute(sql)
        #             conn.commit()
        #             week_num = week_num + 1
        #             print(week_num)
        #             print("WEEK ENDING VALUE UPDATED")
        #
        #
        #         length = len(tx_week)
        #         week_num_plus_one = int(tx_week[4:length]) + 1
        #
        #         print("UPDATING START VALUES: ")
        #         while week_num_plus_one <= 16:
        #             week_plus_one = 'Week ' + str(week_num_plus_one)
        #             c = conn.cursor()
        #             sql = "UPDATE fp_week_start SET {} = '{}'".format(week_plus_one.lower().replace(" ", ""),
        #                                                                                   week_n_ending_value)
        #             print(sql)
        #             c.execute(sql)
        #             conn.commit()
        #             week_num_plus_one = week_num_plus_one + 1
        #             week_n_starting_value = week_n_ending_value








        # #logic to handle if the transaction is for a payout and dollar amount
        # if transaction_type == 'Dollar Amount' and payout_penalty == 'Payout':
        #
        #     #creates the variable to represent the week column that will need to be updated with queries
        #     col_name = 'week'+str(week_num)
        #
        #     #statement to retrieve the current manager's weekly tally for the specific week; reads from the table fp_totals
        #     sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(col_name, manager_name)
        #     manager_week_obj = db_session.execute(sql)
        #
        #     #logic to set the current value of manager's weekly tally
        #     for value in manager_week_obj:
        #         manager_week_current_value = value[0]
        #
        #         #logic to calculate new manager's value for the week that will be used to update the database
        #         if manager_week_current_value == None:
        #             manager_week_update_value = 0 + transaction_value
        #         else:
        #             manager_week_update_value = manager_week_current_value + transaction_value
        #
        #     #sql statement to update the manager's weekly value
        #     sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(col_name,
        #                                                                         manager_week_update_value, manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # statement to retrieve the current manager's total tally for the season; reads from the table fp_totals
        #     sql = "SELECT amount_owed FROM fp_totals WHERE manager_name = '{}'".format(manager_name)
        #     manager_total_obj = db_session.execute(sql)
        #     print(manager_total_obj)
        #
        #     # logic to set the current value of manager's season total tally
        #     for value in manager_total_obj:
        #         print(value)
        #         manager_total_current_value = value[0]
        #
        #         # logic to calculate new manager's total value for the season that will be used to update the database
        #         if manager_total_current_value == None:
        #             manager_total_update_value = 0 + transaction_value
        #         else:
        #             manager_total_update_value = manager_total_current_value + transaction_value
        #
        #     # sql statement to update the manager's total amount value
        #     sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(manager_total_update_value,
        #                                                                           manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     #resest col_name variable
        #     col_name = 'week' + str(week_num)
        #
        #     #sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     #logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     update_value = starting_value - transaction_value
        #
        #     #logic to update all subsequent weeks' starting balances
        #     week_num_it = week_num
        #     while 16-week_num_it >= 0:
        #         col_name_it = 'week' + str(week_num_it)
        #         sql = "UPDATE fp_week_end SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #         week_num_it = week_num_it + 1
        #
        #     # logic to update all subsequent weeks' ending balances
        #     week_num_it = week_num
        #     while 16 - week_num_it > 0:
        #         week_num_it = week_num_it + 1
        #         col_name_it = 'week'+str(week_num_it)
        #         #print(col_name_it)
        #         sql = "UPDATE fp_week_start SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #
        #     #update the final amount (placeholder) column for the starting balance
        #     final_starting_bal = db_session.query(FP_Week_Start).one()
        #     final_starting_bal.placeholder = final_starting_bal.placeholder - transaction_value
        #     db_session.commit()
        #
        #     #update the final amount (placeholder) column for the ending balance
        #     final_ending_bal = db_session.query(FP_Week_End).one()
        #     final_ending_bal.placeholder = final_ending_bal.placeholder - transaction_value
        #     db_session.commit()
        #
        #     #logic to update the overall total pot value
        #     pot_update = db_session.query(FP_Pot).one()
        #     pot_update.pot = pot_update.pot - transaction_value
        #     db_session.commit()
        #
        # elif transaction_type == 'Dollar Amount' and payout_penalty == 'Penalty':
        #     # creates the variable to represent the week column that will need to be updated with queries
        #     col_name = 'week' + str(week_num)
        #
        #     # statement to retrieve the current manager's weekly tally for the specific week; reads from the table fp_totals
        #     sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(col_name, manager_name)
        #     manager_week_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's weekly tally
        #     for value in manager_week_obj:
        #         manager_week_current_value = value[0]
        #
        #         # logic to calculate new manager's value for the week that will be used to update the database
        #         if manager_week_current_value == None:
        #             manager_week_update_value = 0 - transaction_value
        #         else:
        #             manager_week_update_value = manager_week_current_value - transaction_value
        #
        #     # sql statement to update the manager's weekly value
        #     sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(col_name,
        #                                                                           manager_week_update_value,
        #                                                                           manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # statement to retrieve the current manager's total tally for the season; reads from the table fp_totals
        #     sql = "SELECT amount_owed FROM fp_totals WHERE manager_name = '{}'".format(manager_name)
        #     manager_total_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's season total tally
        #     for value in manager_total_obj:
        #         manager_total_current_value = value[0]
        #
        #         # logic to calculate new manager's total value for the season that will be used to update the database
        #         if manager_total_current_value == None:
        #             manager_total_update_value = 0 - transaction_value
        #         else:
        #             manager_total_update_value = manager_total_current_value - transaction_value
        #
        #     # sql statement to update the manager's total amount value
        #     sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(manager_total_update_value,
        #                                                                                    manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # resest col_name variable
        #     col_name = 'week' + str(week_num)
        #
        #     # sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     # logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     update_value = starting_value + transaction_value
        #
        #     # logic to update all subsequent weeks' starting balances
        #     week_num_it = week_num
        #     while 16 - week_num_it >= 0:
        #         col_name_it = 'week' + str(week_num_it)
        #         sql = "UPDATE fp_week_end SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #         week_num_it = week_num_it + 1
        #
        #     # logic to update all subsequent weeks' ending balances
        #     week_num_it = week_num
        #     while 16 - week_num_it > 0:
        #         week_num_it = week_num_it + 1
        #         col_name_it = 'week' + str(week_num_it)
        #         #print(col_name_it)
        #         sql = "UPDATE fp_week_start SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #
        #     # update the final amount (placeholder) column for the starting balance
        #     final_starting_bal = db_session.query(FP_Week_Start).one()
        #     final_starting_bal.placeholder = final_starting_bal.placeholder + transaction_value
        #     db_session.commit()
        #
        #     # update the final amount (placeholder) column for the ending balance
        #     final_ending_bal = db_session.query(FP_Week_End).one()
        #     final_ending_bal.placeholder = final_ending_bal.placeholder + transaction_value
        #     db_session.commit()
        #
        #     # logic to update the overall total pot value
        #     pot_update = db_session.query(FP_Pot).one()
        #     pot_update.pot = pot_update.pot + transaction_value
        #     db_session.commit()
        #
        # elif transaction_type == 'Percentage of Pot' and payout_penalty == 'Penalty':
        #     # creates the variable to represent the week column that will need to be updated with queries
        #     col_name = 'week' + str(week_num)
        #
        #     #calculate transaction value for percentage transactions
        #     # sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     # logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     transaction_value = ((transaction_value / 100) * starting_value)
        #
        #     # statement to retrieve the current manager's weekly tally for the specific week; reads from the table fp_totals
        #     sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(col_name, manager_name)
        #     manager_week_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's weekly tally
        #     for value in manager_week_obj:
        #         manager_week_current_value = value[0]
        #
        #         # logic to calculate new manager's value for the week that will be used to update the database
        #         if manager_week_current_value == None:
        #             manager_week_update_value = 0 - transaction_value
        #         else:
        #             manager_week_update_value = manager_week_current_value - transaction_value
        #
        #     # sql statement to update the manager's weekly value
        #     sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(col_name,
        #                                                                           manager_week_update_value,
        #                                                                           manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # statement to retrieve the current manager's total tally for the season; reads from the table fp_totals
        #     sql = "SELECT amount_owed FROM fp_totals WHERE manager_name = '{}'".format(manager_name)
        #     manager_total_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's season total tally
        #     for value in manager_total_obj:
        #         manager_total_current_value = value[0]
        #
        #         # logic to calculate new manager's total value for the season that will be used to update the database
        #         if manager_total_current_value == None:
        #             manager_total_update_value = 0 - transaction_value
        #         else:
        #             manager_total_update_value = manager_total_current_value - transaction_value
        #
        #     # sql statement to update the manager's total amount value
        #     sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(manager_total_update_value,
        #                                                                                    manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # resest col_name variable
        #     col_name = 'week' + str(week_num)
        #
        #     # sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     # logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     update_value = starting_value + transaction_value
        #
        #     # logic to update all subsequent weeks' starting balances
        #     week_num_it = week_num
        #     while 16 - week_num_it >= 0:
        #         col_name_it = 'week' + str(week_num_it)
        #         sql = "UPDATE fp_week_end SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #         week_num_it = week_num_it + 1
        #
        #     # logic to update all subsequent weeks' ending balances
        #     week_num_it = week_num
        #     while 16 - week_num_it > 0:
        #         week_num_it = week_num_it + 1
        #         col_name_it = 'week' + str(week_num_it)
        #         #print(col_name_it)
        #         sql = "UPDATE fp_week_start SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #
        #     # update the final amount (placeholder) column for the starting balance
        #     final_starting_bal = db_session.query(FP_Week_Start).one()
        #     final_starting_bal.placeholder = final_starting_bal.placeholder + transaction_value
        #     db_session.commit()
        #
        #     # update the final amount (placeholder) column for the ending balance
        #     final_ending_bal = db_session.query(FP_Week_End).one()
        #     final_ending_bal.placeholder = final_ending_bal.placeholder + transaction_value
        #     db_session.commit()
        #
        #     # logic to update the overall total pot value
        #     pot_update = db_session.query(FP_Pot).one()
        #     pot_update.pot = pot_update.pot + transaction_value
        #     db_session.commit()
        #
        # else:
        #     # creates the variable to represent the week column that will need to be updated with queries
        #     col_name = 'week' + str(week_num)
        #
        #     # calculate transaction value for percentage transactions
        #     # sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     # logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     transaction_value = ((transaction_value / 100) * starting_value)
        #
        #     # statement to retrieve the current manager's weekly tally for the specific week; reads from the table fp_totals
        #     sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(col_name, manager_name)
        #     manager_week_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's weekly tally
        #     for value in manager_week_obj:
        #         manager_week_current_value = value[0]
        #
        #         # logic to calculate new manager's value for the week that will be used to update the database
        #         if manager_week_current_value == None:
        #             manager_week_update_value = 0 + transaction_value
        #         else:
        #             manager_week_update_value = manager_week_current_value + transaction_value
        #
        #     # sql statement to update the manager's weekly value
        #     sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(col_name,
        #                                                                           manager_week_update_value,
        #                                                                           manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # statement to retrieve the current manager's total tally for the season; reads from the table fp_totals
        #     sql = "SELECT amount_owed FROM fp_totals WHERE manager_name = '{}'".format(manager_name)
        #     manager_total_obj = db_session.execute(sql)
        #
        #     # logic to set the current value of manager's season total tally
        #     for value in manager_total_obj:
        #         manager_total_current_value = value[0]
        #
        #         # logic to calculate new manager's total value for the season that will be used to update the database
        #         if manager_total_current_value == None:
        #             manager_total_update_value = 0 + transaction_value
        #         else:
        #             manager_total_update_value = manager_total_current_value + transaction_value
        #
        #     # sql statement to update the manager's total amount value
        #     sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(manager_total_update_value,
        #                                                                                    manager_name)
        #     db_session.execute(sql)
        #     db_session.commit()
        #
        #     # resest col_name variable
        #     col_name = 'week' + str(week_num)
        #
        #     # sql statement to the get the starting value for the week of the transaction
        #     sql = "SELECT {} FROM fp_week_start".format(col_name)
        #     starting_object = db_session.execute(sql)
        #
        #     # logic to update the starting balance for the week of the transaction
        #     for value in starting_object:
        #         starting_value = value[0]
        #     update_value = starting_value - transaction_value
        #
        #     # logic to update all subsequent weeks' starting balances
        #     week_num_it = week_num
        #     while 16 - week_num_it >= 0:
        #         col_name_it = 'week' + str(week_num_it)
        #         sql = "UPDATE fp_week_end SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #         week_num_it = week_num_it + 1
        #
        #     # logic to update all subsequent weeks' ending balances
        #     week_num_it = week_num
        #     while 16 - week_num_it > 0:
        #         week_num_it = week_num_it + 1
        #         col_name_it = 'week' + str(week_num_it)
        #         #print(col_name_it)
        #         sql = "UPDATE fp_week_start SET {} = {}".format(col_name_it, update_value)
        #         db_session.execute(sql)
        #         db_session.commit()
        #
        #     # update the final amount (placeholder) column for the starting balance
        #     final_starting_bal = db_session.query(FP_Week_Start).one()
        #     final_starting_bal.placeholder = final_starting_bal.placeholder - transaction_value
        #     db_session.commit()
        #
        #     # update the final amount (placeholder) column for the ending balance
        #     final_ending_bal = db_session.query(FP_Week_End).one()
        #     final_ending_bal.placeholder = final_ending_bal.placeholder - transaction_value
        #     db_session.commit()
        #
        #     # logic to update the overall total pot value
        #     pot_update = db_session.query(FP_Pot).one()
        #     pot_update.pot = pot_update.pot - transaction_value
        #     db_session.commit()
        #
        # flash('Transaction saved')
        # return redirect('/freeparking/')

    results = []
    query = db_session.query(FP_Totals)
    results = query.all()

    for item in results:
        item.week1 = '$' + str("%.2f" % item.week1)
        item.week2 = '$' + str("%.2f" % item.week2)
        item.week3 = '$' + str("%.2f" % item.week3)
        item.week4 = '$' + str("%.2f" % item.week4)
        item.week5 = '$' + str("%.2f" % item.week5)
        item.week6 = '$' + str("%.2f" % item.week6)
        item.week7 = '$' + str("%.2f" % item.week7)
        item.week8 = '$' + str("%.2f" % item.week8)
        item.week9 = '$' + str("%.2f" % item.week9)
        item.week10 = '$' + str("%.2f" % item.week10)
        item.week11 = '$' + str("%.2f" % item.week11)
        item.week12 = '$' + str("%.2f" % item.week12)
        item.week13 = '$' + str("%.2f" % item.week13)
        item.week14 = '$' + str("%.2f" % item.week14)
        item.week15 = '$' + str("%.2f" % item.week15)
        item.week16 = '$' + str("%.2f" % item.week16)
        item.amount_owed = '$' + str("%.2f" % item.amount_owed)
    table = FP_Total_Table(results)
    table.border = True

    pot = []
    query = db_session.query(FP_Pot)
    pot = query.all()

    transactions = []
    query = db_session.query(FP_Transactions)
    transactions = query.all()

    week_start = []
    query = db_session.query(FP_Week_Start)
    week_start = query.all()

    for item in week_start:
        item.week1 = '$' + str("%.2f" % item.week1)
        item.week2 = '$' + str("%.2f" % item.week2)
        item.week3 = '$' + str("%.2f" % item.week3)
        item.week4 = '$' + str("%.2f" % item.week4)
        item.week5 = '$' + str("%.2f" % item.week5)
        item.week6 = '$' + str("%.2f" % item.week6)
        item.week7 = '$' + str("%.2f" % item.week7)
        item.week8 = '$' + str("%.2f" % item.week8)
        item.week9 = '$' + str("%.2f" % item.week9)
        item.week10 = '$' + str("%.2f" % item.week10)
        item.week11 = '$' + str("%.2f" % item.week11)
        item.week12 = '$' + str("%.2f" % item.week12)
        item.week13 = '$' + str("%.2f" % item.week13)
        item.week14 = '$' + str("%.2f" % item.week14)
        item.week15 = '$' + str("%.2f" % item.week15)
        item.week16 = '$' + str("%.2f" % item.week16)
        item.placeholder = '$' + str("%.2f" % item.placeholder)
    table_week_start = FP_Week_Start_Table(week_start)
    table_week_start.border = True

    week_end = []
    query = db_session.query(FP_Week_End)
    week_end = query.all()

    for item in week_end:
        item.week1 = '$' + str("%.2f" % item.week1)
        item.week2 = '$' + str("%.2f" % item.week2)
        item.week3 = '$' + str("%.2f" % item.week3)
        item.week4 = '$' + str("%.2f" % item.week4)
        item.week5 = '$' + str("%.2f" % item.week5)
        item.week6 = '$' + str("%.2f" % item.week6)
        item.week7 = '$' + str("%.2f" % item.week7)
        item.week8 = '$' + str("%.2f" % item.week8)
        item.week9 = '$' + str("%.2f" % item.week9)
        item.week10 = '$' + str("%.2f" % item.week10)
        item.week11 = '$' + str("%.2f" % item.week11)
        item.week12 = '$' + str("%.2f" % item.week12)
        item.week13 = '$' + str("%.2f" % item.week13)
        item.week14 = '$' + str("%.2f" % item.week14)
        item.week15 = '$' + str("%.2f" % item.week15)
        item.week16 = '$' + str("%.2f" % item.week16)
        item.placeholder = '$' + str("%.2f" % item.placeholder)
    table_week_end = FP_Week_End_Table(week_end)
    table_week_end.border = True

    for item in pot:
        item.pot = '$' + str("%.2f" % item.pot)
    table_pot = FP_Pot_Table(pot)
    table_pot.border = True

    table_transactions = FP_Transaction_Table(transactions)
    table_transactions.border = True

    form = FPTransactionForm(formdata=request.form)

    # df['amount'] = df['amount'].map('{:,.2f}'.format)
    # df = df.rename(columns={'name': 'Manager', 'amount': 'Seasonal Total ($)'})
    # data = df.values.tolist()
    # df_html = df.to_html(index=False)  # use pandas method to auto generate html

    #return render_template('freeparking.html', table_html=df_html, data=data)
    return render_template('freeparking2.html', table=[table, table_pot, table_transactions, table_week_start,
                                                       table_week_end], form=form)
    #return render_template('freeparking2.html', table=[table_transactions], form=form)


@app.route('/draft/', methods=["GET","POST"])
def draft():
    form = ArrivalForm(request.form)
    results = []
    query = db_session.query(Arrivals)
    results = query.all()
    table = Arrivals_Table(results)
    table.border = True
    return render_template("draft_bx.html", form=form, table=table)

@app.route('/stats/', methods=["GET","POST"])
def stats():
    return render_template("stats.html")

@app.route('/lifetime_stats/', methods=["GET","POST"])
def lifetime_stats():
    return render_template("lifetime_stats.html")

@app.route('/historic_game_log/', methods=["GET","POST"])
def historic_game_log():
    return render_template("historic_game_log.html")

@app.route('/matchup_analytics/', methods=["GET","POST"])
def matchup_analytics():
    # return render_template("matchup_analytics.html")
    return render_template("matchup_analytics.html")

@app.route('/tests/', methods=["GET","POST"])
def tests():
    # if request.method == "POST":
    #     # try:
    #     cursor, conn = connection()
    #
    #     # except Exception as e:
    #     #    return (str(e))
    #
    #     amendmentName = request.form['amendmentTitle']
    #     managerName = request.form['managerName']
    #     amendment = request.form['amendment']
    #
    #     sql = open("insertAmendment.sql", "r").read().replace('amendment_Name', amendmentName)
    #     sql = sql.replace('manager_Name', managerName)
    #     sql = sql.replace('propasal_text', amendment)
    #     cursor.execute(sql)
    #     conn.commit()
    #     conn.close()
    #     return redirect(url_for('tests'))
    #
    # else:
    #
    #     cursor, conn = connection()
    #     sql = open("proposals.sql", "r").read()
    #     df = pd.read_sql(sql, conn)
    #     conn.close()
    #
    #     df = df.rename(
    #         columns={'amendmentName': 'Amendment Name', 'managerName': 'Manager Name', 'proposal': 'Proposal',
    #                  'status': 'Status'})
    #     data = df.values.tolist()
    #
    #     return render_template("amendments.html", data=data)
    return render_template("index.html")

    # do something to create a pandas datatable
    # try:
    #     cursor, conn = connection()
    #
    # except Exception as e:
    #     return (str(e))
    #
    # sql = open("seasonal_amount.sql", "r").read()
    # df = pd.read_sql(sql, conn)
    # conn.close()
    #
    # df['amount'] = df['amount'].map('{:,.2f}'.format)
    # df = df.rename(columns = {'name': 'Manager', 'amount': 'Seasonal Total ($)'})
    # data = df.values.tolist()
    # print(df)
    #
    # df_html = df.to_html(index=False)  # use pandas method to auto generate html
    #
    # return render_template('test.html', table_html=df_html, data=data)

@app.route('/amendments/', methods=["GET","POST"])
def amendments():
    print(1)
    form = ProposalForm(request.form)
    results = []
    query = db_session.query(Proposal)
    results = query.all()
    print(2)
    if request.method == 'POST': #and form.validate():

        amendmentName = request.form['amendmentTitle']
        managerName = request.form['managerName']
        amendment = request.form['amendment']
        year = '2020'
        proposalStatus = 'Proposed'

        print(amendmentName)
        print(managerName)
        print(amendment)
        print(year)
        print(proposalStatus)

        #print(3)
        # print(form)
        # print(form.proposal_name)
        #proposal = Proposal(form.proposal_name, form.proposal_manager, form.proposal_text, form.proposal_season, form.proposal_status)
        proposal = Proposal(amendmentName, managerName, amendment, year, proposalStatus)
        print(proposal)
        # print(4)
        db_session.add(proposal)
        db_session.commit()
        #save_proposal(proposal, form, new=True)
        flash('Proposal saved')
        return redirect('/amendments/')

    table = Amendment_Table(results)
    table.border = True
    # print(table.__html__())
    return render_template("amendments3.html", form=form, table=table)

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Proposal).filter(
                Proposal.id==id)
    proposal = qry.first()
    if proposal:
        form = ProposalForm(formdata=request.form, obj=proposal)
        if request.method == 'POST' and form.validate():
            # save edits
            save_proposal(proposal, form)
            flash('Proposal updated successfully!')
            return redirect('/amendments/')
        return render_template('edit_proposal.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/arrivalitem/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_arrival(id):
    qry = db_session.query(Arrivals).filter(
                Arrivals.id==id)
    arrival = qry.first()
    if arrival:
        form = ArrivalForm(formdata=request.form, obj=arrival)
        if request.method == 'POST' and form.validate():
            # save edits
            save_arrival(arrival, form)
            flash('Arrival updated successfully!')
            return redirect('/draft/')
        return render_template('edit_arrival.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/fpitem/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fp_transaction(id):
    qry = db_session.query(Arrivals).filter(
                Arrivals.id==id)
    arrival = qry.first()
    if arrival:
        form = ArrivalForm(formdata=request.form, obj=arrival)
        if request.method == 'POST' and form.validate():
            # save edits
            save_arrival(arrival, form)
            flash('Arrival updated successfully!')
            return redirect('/draft/')
        return render_template('edit_arrival.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

# @app.route('/login')
# def login():
#     return render_template('login_bxb.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.user_password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('homepage'))

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        print(email, name, password)

        user = Users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        print(user)

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('signup'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = Users(email=email, user_name=name, user_password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
