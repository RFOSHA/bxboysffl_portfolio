from wtforms import Form, StringField, SelectField, TextAreaField, DecimalField, FloatField

class ProposalForm(Form):
    proposal_statuses = [('Proposed', 'Proposed'),
                   ('Passed', 'Passed'),
                   ('Failed', 'Failed')
                   ]
    seasons = [('2020', '2020')]
    proposal_name = StringField('Proposal Name')
    proposal_manager = StringField('Manager')
    proposal_text = TextAreaField('Proposed Amendment')
    proposal_season = SelectField('Season', choices=seasons)
    proposal_status = SelectField('Status', choices=proposal_statuses)

class ArrivalForm(Form):
    days = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
            ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
    manager_name = StringField('Manger Name')
    day_in = SelectField('Day In', choices=days)
    time_in = StringField('Time In')
    day_out = SelectField('Day Out', choices=days)
    time_out = StringField('Day In')

class FPTransactionForm(Form):
    seasons = [('2020', '2020')]
    managers = [('Ryan', 'Ryan'), ('Nate', 'Nate'), ('Scott', 'Scott'), ('Chris', 'Chris'), ('Max', 'Max'),
                ('Gach', 'Gach'), ('Gwinn', 'Gwinn'), ('DJ', 'DJ'), ('Tom', 'Tom'), ('Ben', 'Ben')]
    pp_choices = [('Payout', 'Payout'),('Penalty', 'Penalty')]
    types = [('Percentage of Pot', 'Percentage of Pot'), ('Dollar Amount', 'Dollar Amount')]
    weeks = [('Week 1', 'Week 1'), ('Week 2', 'Week 2'), ('Week 3', 'Week 3'), ('Week 4', 'Week 4'),
               ('Week 5', 'Week 5'), ('Week 6', 'Week 6'), ('Week 7', 'Week 7'), ('Week 8', 'Week 8'),
               ('Week 9', 'Week 9'), ('Week 10', 'Week 10'), ('Week 11', 'Week 11'), ('Week 12', 'Week 12'),
               ('Week 13', 'Week 13'), ('Week 14', 'Week 14'), ('Week 15', 'Week 15'), ('Week 16', 'Week 16')]
    manager_name = SelectField('Manger Name', choices=managers)
    season = SelectField('Season', choices=seasons)
    week = SelectField('Week', choices=weeks)
    payout_penalty = SelectField('Payout or Penalty', choices=pp_choices)
    transaction_value = FloatField('Transaction Value')
    transaction_type = SelectField('Transaction Type', choices=types)
    transaction_description = TextAreaField('Description')

class RequestForm(Form):
    request_statuses = [('Proposed', 'Proposed'),
                   ('In Progress', 'In Progress'),
                   ('Completed', 'Completed')
                   ]
    request_name = StringField('Request Name')
    request_manager = StringField('Manager')
    request_text = TextAreaField('Request')
    request_status = SelectField('Status', choices=request_statuses)

class BetForm(Form):
    approvals = [('Yes', 'Yes'), ('No', 'No')]
    seasons = [('2020', '2020')]
    managers = [('Ryan', 'Ryan'), ('Nate', 'Nate'), ('Scott', 'Scott'), ('Chris', 'Chris'), ('Max', 'Max'),
                ('Gach', 'Gach'), ('Gwinn', 'Gwinn'), ('DJ', 'DJ'), ('Tom', 'Tom'), ('Ben', 'Ben')]
    bet_outcomes = [('Accepted', 'Accepted'),
                   ('Cancelled', 'Cancelled'),
                   ('Manager 1 Won', 'Manager 1 Won'),
                   ('Manager 2 Won', 'Manager 2 Won')
                   ]
    manager_name1 = SelectField('Manger 1 Name', choices=managers)
    manager_name2 = SelectField('Manager 2 Name', choices=managers)
    bet_desc = TextAreaField('Bet Description')
    bet_amount = StringField('Bet Amount')
    manager1_approval = SelectField('Manger 1 Approval', choices=approvals)
    manager2_approval = SelectField('Manger 2 Approval', choices=approvals)
    season = SelectField('Season', choices=seasons)
    bet_outcome = SelectField('Outcome', choices=bet_outcomes)