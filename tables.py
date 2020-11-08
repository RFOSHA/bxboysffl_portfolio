from flask_table import Table, Col, LinkCol, ButtonCol
import locale
from flask import url_for

class CurrencyCol(Col):
    def td_format(self, content):
        amount = float(content)
        locale.setlocale(locale.LC_NUMERIC)
        val = locale.format_string('%.2f', float(amount))
        return f'${val}'

class Amendment_Table(Table):
    id = Col('Id', show=False)
    proposal_name = Col('Proposal Name', column_html_attrs={'width': '10%'})
    proposal_manager = Col('Manager', column_html_attrs={'width': '10%'})
    proposal_text = Col('Proposed Amendment', column_html_attrs={'width': '50%'})
    proposal_season = Col('Season', column_html_attrs={'width': '10%'})
    proposal_status = Col('Status',column_html_attrs={'width': '10%'})
    #edit = ButtonCol('Edit', 'edit', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'),anchor_attrs={'type': 'button',
                                 'class': 'btn btn-primary'}, column_html_attrs={'width': '10%'})

class FP_Total_Table(Table):
    id = Col('Id', show=False)
    manager_name = Col('Manger')
    week1 = CurrencyCol('Week 1')
    week2 = CurrencyCol('Week 2')
    week3 = CurrencyCol('Week 3')
    week4 = CurrencyCol('Week 4')
    week5 = CurrencyCol('Week 5')
    week6 = CurrencyCol('Week 6')
    week7 = CurrencyCol('Week 7')
    week8 = CurrencyCol('Week 8')
    week9 = CurrencyCol('Week 9')
    week10 = CurrencyCol('Week 10')
    week11 = CurrencyCol('Week 11')
    week12 = CurrencyCol('Week 12')
    week13 = CurrencyCol('Week 13')
    week14 = CurrencyCol('Week 14')
    week15 = CurrencyCol('Week 15')
    week16 = CurrencyCol('Week 16')
    amount_owed = CurrencyCol('Amount')

class Arrivals_Table(Table):
    id = Col('Id', show=False)
    manager_name = Col('Manger')
    day_in = Col('Day In')
    time_in = Col('Time In')
    day_out = Col('Day Out')
    time_out = Col('Time Out')
    edit = LinkCol('Edit', 'edit_arrival', url_kwargs=dict(id='id'),anchor_attrs={'type': 'button',
                                 'class': 'btn btn-primary'}, column_html_attrs={'width': '10%'})

class FP_Pot_Table(Table):
    id = Col('Id', show=False)
    pot = CurrencyCol('Free Parking Pot')

class FP_Transaction_Table(Table):
    id = Col('Id', show=False)
    manager_name = Col('Manager Name')
    season = Col('Season')
    week = Col('Week')
    payout_penalty = Col('Payout or Penalty')
    transaction_value = Col('Transaction Value')
    transaction_type = Col('Transaction Type')
    transaction_description = Col('Transaction Description')

class Bets_Table(Table):
    id = Col('Id', show=False)
    manager_name_1 = Col('Manager Name 1')
    manager_name_2 = Col('Manager Name 2')
    bet = Col('The Bet')
    amount = Col('Bet Amount')
    manager_name_1_signed = ('Manager 1 Verification')
    manager_name_2_signed = ('Manager 2 Verification')

class FP_Week_Start_Table(Table):
    id = Col('Id', show=False)
    starting_balance = Col('')
    week1 = CurrencyCol('Week 1')
    week2 = CurrencyCol('Week 2')
    week3 = CurrencyCol('Week 3')
    week4 = CurrencyCol('Week 4')
    week5 = CurrencyCol('Week 5')
    week6 = CurrencyCol('Week 6')
    week7 = CurrencyCol('Week 7')
    week8 = CurrencyCol('Week 8')
    week9 = CurrencyCol('Week 9')
    week10 = CurrencyCol('Week 10')
    week11 = CurrencyCol('Week 11')
    week12 = CurrencyCol('Week 12')
    week13 = CurrencyCol('Week 13')
    week14 = CurrencyCol('Week 14')
    week15 = CurrencyCol('Week 15')
    week16 = CurrencyCol('Week 16')
    placeholder = CurrencyCol('Final Amount')

class FP_Week_End_Table(Table):
    id = Col('Id', show=False)
    ending_balance = Col('')
    week1 = CurrencyCol('Week 1')
    week2 = CurrencyCol('Week 2')
    week3 = CurrencyCol('Week 3')
    week4 = CurrencyCol('Week 4')
    week5 = CurrencyCol('Week 5')
    week6 = CurrencyCol('Week 6')
    week7 = CurrencyCol('Week 7')
    week8 = CurrencyCol('Week 8')
    week9 = CurrencyCol('Week 9')
    week10 = CurrencyCol('Week 10')
    week11 = CurrencyCol('Week 11')
    week12 = CurrencyCol('Week 12')
    week13 = CurrencyCol('Week 13')
    week14 = CurrencyCol('Week 14')
    week15 = CurrencyCol('Week 15')
    week16 = CurrencyCol('Week 16')
    placeholder = CurrencyCol('Final Amount')

class Request_Table(Table):
    id = Col('Id', show=False)
    request_name = Col('Request Name')
    request_manager = Col('Requester')
    request_text = Col('Requeset')
    request_status = Col('Request Status')
    edit = LinkCol('Edit', 'edit_request', url_kwargs=dict(id='id'),anchor_attrs={'type': 'button',
                                 'class': 'btn btn-primary'}, column_html_attrs={'width': '10%'})

class Bet_Table(Table):
    id = Col('Id', show=False)
    manager_name1 = Col('Manger 1')
    manager_name2 = Col('Manger 2')
    bet_desc = Col('Bet')
    bet_amount = Col('Amount')
    manager1_approval = Col('Manger 1 Approval')
    manager2_approval = Col('Manger 2 Approval')
    season = Col('Season')
    bet_outcome = Col('Outcome')
    edit = LinkCol('Edit', 'edit_bet', url_kwargs=dict(id='id'),anchor_attrs={'type': 'button',
                                 'class': 'btn btn-primary'}, column_html_attrs={'width': '10%'})

class Lifetime_Stats_Table(Table):
    index = Col('Id', show=False)
    manager = Col('Manger')
    record_overall_pointsFor = Col('Points For')
    record_overall_pointsAgainst = Col('Points Against')
    record_overall_wins = Col('Wins')
    record_overall_losses = Col('Losses')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('lifetime_stats', sort=col_key, direction=direction)

class Matchup_Stats_Table(Table):
    id = Col('Id', show=False)
    head_to_head_matchup = Col('Matchup')
    wins = Col('Wins')
    losses = Col('Losses')
    tie = Col('Ties')
    points_for = Col('Points For')
    points_against = Col('Points Against')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('matchup_analytics', sort=col_key, direction=direction)

# class SortableTable(Table):
#     id = Col('ID')
#     name = Col('Name')
#     description = Col('Description')
#     link = LinkCol(
#         'Link', 'flask_link', url_kwargs=dict(id='id'), allow_sort=False)
#     allow_sort = True








