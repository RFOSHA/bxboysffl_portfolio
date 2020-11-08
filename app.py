from config import app
from db_setup import init_db, db_session
from forms import ProposalForm, ArrivalForm, FPTransactionForm, RequestForm, BetForm
from flask import flash, render_template, request, redirect, url_for
from models import Proposal, Users, FP_Totals, Arrivals, FP_Pot, FP_Transactions, FP_Week_End, \
    FP_Week_Start, Requests, SideBets, Lifetime_Stats, Matchup_Stats
from tables import Amendment_Table, FP_Total_Table, Arrivals_Table, FP_Pot_Table, FP_Transaction_Table, \
    FP_Week_End_Table, FP_Week_Start_Table, Request_Table, Bet_Table, Lifetime_Stats_Table, Matchup_Stats_Table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import pyodbc
from sqlalchemy import desc, asc

driver = "{ODBC Driver 17 for SQL Server}"
server = "bxboysdbserver.database.windows.net"
database = "bxboysdb_portfolio"
username = "rfosha"
pwd = "Bxboys2020"

# Construct connection string
conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+pwd

init_db()

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.user_password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for('homepage'))

    return render_template('login2.html')

@app.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    # return render_template('login_template.html')
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        # remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(email=email).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.user_password, current_password):
            flash('Please check your login details and try again.')
            return redirect(url_for('change_password'))  # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        if new_password != confirm_password:
            flash('Your new passwords did not match. Try again.')
            return redirect(url_for('change_password'))
        else:
            # create new user with the form data. Hash the password so plaintext version isn't saved.
            # conn = pyodbc.connect(conn_string)
            # c = conn.cursor()
            # hashed_password = generate_password_hash(new_password, method='sha256')
            # sql = "UPDATE users SET user_password = '{}' WHERE email = '{}'".format(hashed_password, email)
            # c.execute(sql)
            # conn.commit()
            # c.close()
            # conn.close()

            flash('Sorry, guests cannot change the password')
            return redirect(url_for('change_password'))

    return render_template('change_password.html')

@app.route('/bylaws/', methods = ['GET', 'POST'])
@login_required
def bylaws():
    return render_template("bylaws.html")

@app.route('/homepage/', methods=["GET","POST"])
@login_required
def homepage():
    return render_template("index.html")

@app.route('/freeparking/', methods=["GET","POST"])
@login_required
def freeparking():
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',
             'Week 9', 'Week 10', 'Week 11', 'Week 12', 'Week 13', 'Week14', 'Week 15', 'Week 16']

    #gets data from the transaction input form
    if request.method == 'POST':
        # conn = sqlite3.connect("bxboys.db")
        # conn = pyodbc.connect(conn_string)

        manager_name = request.form['manager_name']
        season = request.form['season']
        tx_week = request.form['week']
        payout_penalty = request.form['payout_penalty']
        transaction_value = request.form['transaction_value']
        transaction_value = float(transaction_value)
        transaction_type = request.form['transaction_type']
        transaction_description = request.form['transaction_description']

        c = conn.cursor()
        sql = "INSERT INTO fp_transaction (manager_name, season, week, payout_penalty, transaction_value," \
              "transaction_type, transaction_description) " \
              "VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}')".format(manager_name, season, tx_week, payout_penalty,
                                                           transaction_value, transaction_type, transaction_description)
        print(sql)
        c.execute(sql)
        conn.commit()
        c.close()

        c = conn.cursor()
        sql = "SELECT {} FROM fp_totals WHERE manager_name = '{}'".format(tx_week.lower().replace(" ", ""),
                                                                          manager_name)
        c.execute(sql)
        week_n_manager_object = c.fetchall()
        for row in week_n_manager_object:
            week_n_manager_value = float(row[0])
            print("Manager (" + str(manager_name + ") STARTING VALUE:"))
            print(week_n_manager_value)
        c.close()

        c = conn.cursor()
        sql = "SELECT {} FROM fp_week_start".format(tx_week.lower().replace(" ", ""))
        c.execute(sql)
        week_n_starting_object = c.fetchall()
        for row in week_n_starting_object:
            week_n_starting_value_man = float(row[0])
            print(str(tx_week) + "STARTING VALUE:")
            print(week_n_starting_value_man)
        c.close()

        if transaction_type == 'Dollar Amount' and payout_penalty == 'Payout':
            week_n_manager_update = float(week_n_manager_value - transaction_value)
        elif transaction_type == 'Dollar Amount' and payout_penalty == 'Penalty':
            week_n_manager_update = float(week_n_manager_value + transaction_value)
        elif transaction_type == 'Percentage of Pot' and payout_penalty == 'Payout':
            week_n_manager_update = float(week_n_manager_value - ((transaction_value / 100) * week_n_starting_value_man))
        else:
            week_n_manager_update = float(week_n_manager_value + ((transaction_value / 100) * week_n_starting_value_man))

        c = conn.cursor()
        sql = "UPDATE fp_totals SET {} = {} WHERE manager_name = '{}'".format(tx_week.lower().replace(" ", ""),
                                                                              week_n_manager_update, manager_name)
        print("SQL: ")
        print(sql)
        c.execute(sql)
        conn.commit()
        c.close()

        for week in weeks:
            c = conn.cursor()
            sql = "SELECT {} FROM fp_week_start".format(week.lower().replace(" ", ""))
            c.execute(sql)
            week_n_starting_object = c.fetchall()
            for row in week_n_starting_object:
                week_n_starting_value = float(row[0])
                print(str(week) + " STARTING VALUE:")
                print(week_n_starting_value)
            c.close()

            c = conn.cursor()
            sql = "SELECT {} FROM fp_totals".format(week.lower().replace(" ", ""))
            c.execute(sql)
            transactions_for_week_n_obj = c.fetchall()

            week_total = 0

            for transaction in transactions_for_week_n_obj:
                print("TRANSACTION:")
                print(transaction[0])
                week_total = float(week_total + transaction[0])
                print(week)

            week_total = float(week_n_starting_value + week_total)
            c.close()

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
            c.close()
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
                c.close()

        c = conn.cursor()
        sql = "SELECT * FROM fp_totals"
        print("SQL: ")
        print(sql)
        c.execute(sql)
        manager_totals_obj = c.fetchall()

        for manager_item in manager_totals_obj:
            print('MANAGER:')
            print(manager_item)
            i = 2
            total = 0
            while i < 18:
                total = float(total + manager_item[i])
                i += 1

            c = conn.cursor()
            sql = "UPDATE fp_totals SET amount_owed = {} WHERE manager_name = '{}'".format(total, manager_item[1])
            print("SQL: ")
            print(sql)
            c.execute(sql)
            conn.commit()

        c.close()
        c = conn.cursor()
        sql = "SELECT week16 FROM fp_week_end"
        c.execute(sql)
        final_end_value_obj = c.fetchall()

        for value in final_end_value_obj:
            final_end_value = float(value[0])
            print(final_end_value)
            print("IM HERE")
        sql = "UPDATE fp_week_end SET placeholder = {}".format(final_end_value)
        c.execute(sql)
        conn.commit()
        c.close()

        sql = "UPDATE fp_week_start SET placeholder = {}".format(final_end_value)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        c.close()

        sql = "UPDATE fp_pot SET pot = {}".format(final_end_value)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

        flash('Transaction saved')
        return redirect('/freeparking/')

    # results = []
    # conn = psycopg2.connect(conn_string)
    # c = conn.cursor()
    # sql = "SELECT * FROM fp_totals"
    # print("SQL: ")
    # print(sql)
    # c.execute(sql)
    # results = c.fetchall()
    # print(results)
    # print(type(results))

    # for manager_item in manager_totals_obj:
    #     print('MANAGER:')
    #     print(manager_item)

    results = []
    query = db_session.query(FP_Totals)
    results = query.all()

    db_session.close()

    # for item in results:
    #     item.week1 = '$' + str("%.2f" % item.week1)
    #     item.week2 = '$' + str("%.2f" % item.week2)
    #     item.week3 = '$' + str("%.2f" % item.week3)
    #     item.week4 = '$' + str("%.2f" % item.week4)
    #     item.week5 = '$' + str("%.2f" % item.week5)
    #     item.week6 = '$' + str("%.2f" % item.week6)
    #     item.week7 = '$' + str("%.2f" % item.week7)
    #     item.week8 = '$' + str("%.2f" % item.week8)
    #     item.week9 = '$' + str("%.2f" % item.week9)
    #     item.week10 = '$' + str("%.2f" % item.week10)
    #     item.week11 = '$' + str("%.2f" % item.week11)
    #     item.week12 = '$' + str("%.2f" % item.week12)
    #     item.week13 = '$' + str("%.2f" % item.week13)
    #     item.week14 = '$' + str("%.2f" % item.week14)
    #     item.week15 = '$' + str("%.2f" % item.week15)
    #     item.week16 = '$' + str("%.2f" % item.week16)
    #     item.amount_owed = '$' + str("%.2f" % item.amount_owed)
    table = FP_Total_Table(results)
    table.border = True
    # c.close()

    # pot = []
    # conn = psycopg2.connect(conn_string)
    # c = conn.cursor()
    # sql = "SELECT * FROM fp_pot"
    # print("SQL: ")
    # print(sql)
    # c.execute(sql)
    # pot = c.fetchall()

    pot = []
    query = db_session.query(FP_Pot)
    pot = query.all()
    db_session.close()

    # for item in pot:
    #     item.pot = '$' + str("%.2f" % item.pot)
    table_pot = FP_Pot_Table(pot)
    table_pot.border = True
    # c.close()

    # transactions = []
    # conn = psycopg2.connect(conn_string)
    # c = conn.cursor()
    # sql = "SELECT * FROM fp_transaction"
    # print("SQL: ")
    # print(sql)
    # c.execute(sql)
    # transactions = c.fetchall()

    transactions = []
    query = db_session.query(FP_Transactions).order_by(asc(FP_Transactions.id))
    transactions = query.all()
    db_session.close()

    # for item in transactions:
    #     if item.transaction_type == 'Dollar Amount':
    #         item.transaction_value = '$' + str("%.2f" % item.transaction_value)
    #     else:
    #         item.transaction_value = str(item.transaction_value) + '%'
    table_transactions = FP_Transaction_Table(transactions)
    table_transactions.border = True
    # c.close()

    # week_start = []
    # conn = psycopg2.connect(conn_string)
    # c = conn.cursor()
    # sql = "SELECT * FROM fp_week_start"
    # print("SQL: ")
    # print(sql)
    # c.execute(sql)
    # week_start = c.fetchall()

    week_start = []
    query = db_session.query(FP_Week_Start)
    week_start = query.all()
    db_session.close()

    # for item in week_start:
    #     item.week1 = '$' + str("%.2f" % item.week1)
    #     item.week2 = '$' + str("%.2f" % item.week2)
    #     item.week3 = '$' + str("%.2f" % item.week3)
    #     item.week4 = '$' + str("%.2f" % item.week4)
    #     item.week5 = '$' + str("%.2f" % item.week5)
    #     item.week6 = '$' + str("%.2f" % item.week6)
    #     item.week7 = '$' + str("%.2f" % item.week7)
    #     item.week8 = '$' + str("%.2f" % item.week8)
    #     item.week9 = '$' + str("%.2f" % item.week9)
    #     item.week10 = '$' + str("%.2f" % item.week10)
    #     item.week11 = '$' + str("%.2f" % item.week11)
    #     item.week12 = '$' + str("%.2f" % item.week12)
    #     item.week13 = '$' + str("%.2f" % item.week13)
    #     item.week14 = '$' + str("%.2f" % item.week14)
    #     item.week15 = '$' + str("%.2f" % item.week15)
    #     item.week16 = '$' + str("%.2f" % item.week16)
    #     item.placeholder = '$' + str("%.2f" % item.placeholder)
    table_week_start = FP_Week_Start_Table(week_start)
    table_week_start.border = True
    # c.close()

    # week_end = []
    # conn = psycopg2.connect(conn_string)
    # c = conn.cursor()
    # sql = "SELECT * FROM fp_week_end"
    # print("SQL: ")
    # print(sql)
    # c.execute(sql)
    # week_end = c.fetchall()

    week_end = []
    query = db_session.query(FP_Week_End)
    week_end = query.all()
    db_session.close()

    # for item in week_end:
    #     item.week1 = '$' + str("%.2f" % item.week1)
    #     item.week2 = '$' + str("%.2f" % item.week2)
    #     item.week3 = '$' + str("%.2f" % item.week3)
    #     item.week4 = '$' + str("%.2f" % item.week4)
    #     item.week5 = '$' + str("%.2f" % item.week5)
    #     item.week6 = '$' + str("%.2f" % item.week6)
    #     item.week7 = '$' + str("%.2f" % item.week7)
    #     item.week8 = '$' + str("%.2f" % item.week8)
    #     item.week9 = '$' + str("%.2f" % item.week9)
    #     item.week10 = '$' + str("%.2f" % item.week10)
    #     item.week11 = '$' + str("%.2f" % item.week11)
    #     item.week12 = '$' + str("%.2f" % item.week12)
    #     item.week13 = '$' + str("%.2f" % item.week13)
    #     item.week14 = '$' + str("%.2f" % item.week14)
    #     item.week15 = '$' + str("%.2f" % item.week15)
    #     item.week16 = '$' + str("%.2f" % item.week16)
    #     item.placeholder = '$' + str("%.2f" % item.placeholder)
    table_week_end = FP_Week_End_Table(week_end)
    table_week_end.border = True
    # c.close()

    form = FPTransactionForm(formdata=request.form)

    return render_template('freeparking2.html', table=[table, table_pot, table_transactions, table_week_start,
                                                       table_week_end], form=form)


@app.route('/draft/', methods=["GET", "POST"])
def draft():
    form = ArrivalForm(request.form)
    results = []
    query = db_session.query(Arrivals)
    results = query.all()
    table = Arrivals_Table(results)
    table.border = True
    db_session.close()
    return render_template("draft_bx.html", form=form, table=table)


@app.route('/stats/', methods=["GET","POST"])
def stats():
    return render_template("coming_soon.html")

@app.route('/historic_game_log/', methods=["GET","POST"])
def historic_game_log():
    return render_template("coming_soon.html")

@app.route('/bets/', methods=["GET","POST"])
def bets():
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    form = BetForm(request.form)
    results = []
    query = db_session.query(SideBets).order_by(asc(SideBets.id))
    results = query.all()

    if request.method == 'POST':  # and form.validate():

        manager_name1 = request.form['manager_name1']
        manager_name2 = request.form['manager_name2']
        bet_desc = request.form['bet_desc']
        bet_amount = request.form['bet_amount']
        manager1_approval = request.form['manager1_approval']
        manager2_approval = request.form['manager2_approval']
        season = request.form['season']
        bet_outcome = request.form['bet_outcome']

        #bet = SideBets(manager_name1, manager_name2, bet_desc, bet_amount, manager1_approval, manager2_approval, season, bet_outcome)

        sql = "INSERT INTO side_bets (manager_name1, manager_name2, bet_desc, bet_amount, manager1_approval, " \
              "manager2_approval, season, bet_outcome) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
              "'{}')".format(manager_name1, manager_name2, bet_desc, bet_amount, manager1_approval, manager2_approval, season, bet_outcome)
        c.execute(sql)
        conn.commit()
        c.close()

        # try:
        #     db_session.add(bet)
        #     db_session.commit()
        #     db_session.close()
        # except:
        #     db_session.rollback()
        #     raise
        # finally:
        #     db_session.close()
        flash('Bet saved')
        return redirect('/bets/')

    table = Bet_Table(results)
    table.border = True
    db_session.close()
    return render_template("bets.html", form=form, table=table)


@app.route('/site_requests/', methods=["GET","POST"])
def site_requests():
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    form = RequestForm(request.form)
    results = []
    query = db_session.query(Requests).order_by(asc(Requests.id))
    results = query.all()

    if request.method == 'POST':  # and form.validate():

        requestName = request.form['requestName']
        managerName = request.form['managerName']
        request_text = request.form['request_text']
        requestStatus = 'Proposed'

        # site_request = Requests(requestName, managerName, request_text, requestStatus)

        sql = "INSERT INTO requests (request_name, request_manager, request_text, request_status) " \
              "VALUES ('{}', '{}', '{}', '{}')".format(requestName, managerName, request_text, requestStatus)
        c.execute(sql)
        conn.commit()
        c.close()

        # try:
        #     db_session.add(site_request)
        #     db_session.commit()
        # except:
        #     db_session.rollback()
        #     raise
        # finally:
        #     db_session.close()
        flash('Request saved')
        return redirect('/site_requests/')

    table = Request_Table(results)
    table.border = True
    db_session.close()
    return render_template("requests.html", form=form, table=table)

@app.route('/amendments/', methods=["GET","POST"])
def amendments():
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    form = ProposalForm(request.form)
    results = []
    query = db_session.query(Proposal).order_by(asc(Proposal.id))
    results = query.all()

    if request.method == 'POST': #and form.validate():

        amendmentName = request.form['amendmentTitle']
        managerName = request.form['managerName']
        amendment = request.form['amendment']
        year = '2020'
        proposalStatus = 'Proposed'

        # proposal = Proposal(amendmentName, managerName, amendment, year, proposalStatus)

        sql = "INSERT INTO proposals (proposal_name, proposal_manager, proposal_text, proposal_season, proposal_status) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}')".format(amendmentName, managerName, amendment, year, proposalStatus)
        c.execute(sql)
        conn.commit()
        c.close()

        # try:
        #     db_session.add(proposal)
        #     db_session.commit()
        # except:
        #     db_session.rollback()
        #     raise
        # finally:
        #     db_session.close()
        #     db_session.remove()

        flash('Proposal saved')
        return redirect('/amendments/')

    table = Amendment_Table(results)
    table.border = True
    db_session.close()
    return render_template("amendments3.html", form=form, table=table)

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    qry = db_session.query(Proposal).filter(
                Proposal.id==id)
    proposal = qry.first()

    if proposal:
        form = ProposalForm(formdata=request.form, obj=proposal)
        if request.method == 'POST' and form.validate():
            # save edits
            proposal_name = form.proposal_name.data
            proposal_manager = form.proposal_manager.data
            proposal_text = form.proposal_text.data
            proposal_season = form.proposal_season.data
            proposal_status = form.proposal_status.data

            sql = "UPDATE proposals SET proposal_name = '{}',  proposal_manager = '{}',  proposal_text = '{}', " \
                  "proposal_season = '{}', proposal_status = '{}' " \
                  "WHERE id = '{}'".format(proposal_name, proposal_manager, proposal_text, proposal_season, proposal_status, id)
            c.execute(sql)
            conn.commit()
            c.close()

            # save_proposal(proposal, form)
            flash('Proposal updated successfully!')
            return redirect('/amendments/')
        return render_template('edit_proposal.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    db_session.close()


@app.route('/arrivalitem/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_arrival(id):
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    qry = db_session.query(Arrivals).filter(
                Arrivals.id==id)
    arrival = qry.first()

    if arrival:
        form = ArrivalForm(formdata=request.form, obj=arrival)
        if request.method == 'POST' and form.validate():
            # save edits
            manager_name = form.manager_name.data
            day_in = form.day_in.data
            time_in = form.time_in.data
            day_out = form.day_out.data
            time_out = form.time_out.data

            sql = "UPDATE arrivals SET manager_name = '{}',  day_in = '{}',  time_in = '{}', " \
                  "day_out = '{}', time_out = '{}' " \
                  "WHERE id = '{}'".format(manager_name, day_in, time_in, day_out, time_out, id)
            c.execute(sql)
            conn.commit()
            c.close()

            flash('Arrival updated successfully!')
            return redirect('/draft/')
        return render_template('edit_arrival.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    db_session.close()

@app.route('/fpitem/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fp_transaction(id):
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    qry = db_session.query(Arrivals).filter(
                Arrivals.id==id)
    arrival = qry.first()

    if arrival:
        form = ArrivalForm(formdata=request.form, obj=arrival)
        if request.method == 'POST' and form.validate():
            # save edits
            manager_name = form.manager_name.data
            day_in = form.day_in.data
            time_in = form.time_in.data
            day_out = form.day_out.data
            time_out = form.time_out.data

            sql = "UPDATE arrivals SET manager_name = '{}',  day_in = '{}',  time_in = '{}', " \
                  "day_out = '{}',  time_out = '{}'" \
                  "WHERE id = '{}'".format(manager_name, day_in, time_in, day_out, time_out, id)

            c.execute(sql)
            conn.commit()
            c.close()

            flash('Arrival updated successfully!')
            return redirect('/draft/')
        return render_template('edit_arrival.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    db_session.close()

@app.route('/request/<int:id>', methods=['GET', 'POST'])
def edit_request(id):
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    qry = db_session.query(Requests).filter(
                Requests.id==id)
    site_request = qry.first()

    if site_request:
        form = RequestForm(formdata=request.form, obj=site_request)
        if request.method == 'POST' and form.validate():
            # save edits
            request_name = form.request_name.data
            request_manager = form.request_manager.data
            request_text = form.request_text.data
            request_status = form.request_status.data

            sql = "UPDATE requests SET request_name = '{}',  request_manager = '{}',  request_text = '{}', " \
                  "request_status = '{}' " \
                  "WHERE id = '{}'".format(request_name, request_manager, request_text, request_status, id)
            c.execute(sql)
            conn.commit()
            c.close()

            # save_request(site_request, form)
            flash('Request updated successfully!')
            return redirect('/site_requests/')
        return render_template('edit_request.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    db_session.close()

@app.route('/bet/<int:id>', methods=['GET', 'POST'])
def edit_bet(id):
    conn = pyodbc.connect(conn_string)
    c = conn.cursor()

    qry = db_session.query(SideBets).filter(
                SideBets.id==id)
    bet = qry.first()
    if bet:
        form = BetForm(formdata=request.form, obj=bet)
        if request.method == 'POST' and form.validate():
            # save edits
            manager_name1 = form.manager_name1.data
            manager_name2 = form.manager_name2.data
            bet_desc = form.bet_desc.data
            bet_amount = form.bet_amount.data
            manager1_approval = form.manager1_approval.data
            manager2_approval = form.manager2_approval.data
            season = form.season.data
            bet_outcome = form.bet_outcome.data

            sql = "UPDATE side_bets SET manager_name1 = '{}',  manager_name2 = '{}',  bet_desc = '{}', " \
                  "bet_amount = '{}', manager1_approval = '{}', manager2_approval = '{}', season = '{}', bet_outcome = '{}' " \
                  "WHERE id = '{}'".format(manager_name1, manager_name2, bet_desc, bet_amount, manager1_approval, manager2_approval, season, bet_outcome, id)
            c.execute(sql)
            conn.commit()
            c.close()

            # save_bet(bet, form)
            flash('Bet updated successfully!')
            return redirect('/bets/')
        return render_template('edit_bet.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
    db_session.close()

###SIGNUP
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     conn = pyodbc.connect(conn_string)
#     c = conn.cursor()
#     if request.method == 'POST':
#         email = request.form.get('email')
#         name = request.form.get('name')
#         password = request.form.get('password')
#         password = generate_password_hash(password, method='sha256')
#         print(email, name, password)
#
#         user = Users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
#         print(user)
#
#         if user: # if a user is found, we want to redirect back to signup page so user can try again
#             flash('Email address already exists')
#             return redirect(url_for('signup'))
#
#         # create new user with the form data. Hash the password so plaintext version isn't saved.
#         new_user = Users(email=email, user_name=name, user_password=generate_password_hash(password, method='sha256'))
#
#         sql = "INSERT INTO users (email, user_name, user_password) " \
#               "VALUES ('{}', '{}', '{}')".format(email, name, password)
#         c.execute(sql)
#         conn.commit()
#         c.close()
#
#
#         return redirect(url_for('login'))
#
#     return render_template('signup.html')

@app.route('/lifetime_stats/', methods=["GET","POST"])
def lifetime_stats():
    sort = request.args.get('sort', 'index')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    conn = pyodbc.connect(conn_string)
    c = conn.cursor()
    table = Lifetime_Stats_Table(Lifetime_Stats.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    table.border = True
    db_session.close()
    return render_template("lifetime_stats.html", table=table)

@app.route('/matchup_analytics/', methods=["GET","POST"])
def matchup_analytics():
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    conn = pyodbc.connect(conn_string)
    c = conn.cursor()
    table = Matchup_Stats_Table(Matchup_Stats.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    table.border = True
    db_session.close()
    return render_template("matchup_analytics.html", table=table)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
