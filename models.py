from config import db
from flask_login import UserMixin
from db_setup import db_session
from sqlalchemy import desc

class Proposal(db.Model):
    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key=True)
    proposal_name = db.Column(db.String)
    proposal_manager = db.Column(db.String)
    proposal_text = db.Column(db.String)
    proposal_season = db.Column(db.String)
    proposal_status = db.Column(db.String)

    def __init__(self, proposal_name, proposal_manager, proposal_text, proposal_season, proposal_status):
        self.proposal_name = proposal_name
        self.proposal_manager = proposal_manager
        self.proposal_text = proposal_text
        self.proposal_season = proposal_season
        self.proposal_status = proposal_status

    def __repr__(self):
        return "<Proposal: {}>".format(self.proposal_name)


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    user_name = db.Column(db.String)
    user_password = db.Column(db.String)

    def __init__(self, email, user_name, user_password):
        self.email = email
        self.user_name = user_name
        self.user_password = user_password


    def __repr__(self):
        return "<Users: {}>".format(self.user_name)


class FP_Totals(db.Model):
    __tablename__ = "fp_totals"

    id = db.Column(db.Integer, primary_key=True)
    manager_name = db.Column(db.String)
    week1 = db.Column(db.Float)
    week2 = db.Column(db.Float)
    week3 = db.Column(db.Float)
    week4 = db.Column(db.Float)
    week5 = db.Column(db.Float)
    week6 = db.Column(db.Float)
    week7 = db.Column(db.Float)
    week8 = db.Column(db.Float)
    week9 = db.Column(db.Float)
    week10 = db.Column(db.Float)
    week11 = db.Column(db.Float)
    week12 = db.Column(db.Float)
    week13 = db.Column(db.Float)
    week14 = db.Column(db.Float)
    week15 = db.Column(db.Float)
    week16 = db.Column(db.Float)
    amount_owed = db.Column(db.Float)

    def __init__(self, manager_name, amount_owed):
        self.manager_name = manager_name
        self.amount_owed = amount_owed


    def __repr__(self):
        return "<FP_Totals: {}>".format(self.manager_name)

class Arrivals(db.Model):
    __tablename__ = "arrivals"

    id = db.Column(db.Integer, primary_key=True)
    manager_name = db.Column(db.String)
    day_in = db.Column(db.String)
    time_in = db.Column(db.String)
    day_out = db.Column(db.String)
    time_out = db.Column(db.String)

    def __init__(self, manager_name, day_in, time_in, day_out, time_out):
        self.manager_name = manager_name
        self.day_in = day_in
        self.time_in = time_in
        self.day_out = day_out
        self.time_out = time_out


    def __repr__(self):
        return "<Arrivals: {}>".format(self.manager_name)

class FP_Pot(db.Model):
    __tablename__ = "fp_pot"

    id = db.Column(db.Integer, primary_key=True)
    pot = db.Column(db.Float)

    def __init__(self, pot):
        self.pot = pot


    def __repr__(self):
        return "<FP_Pot: {}>".format(self.pot)

class FP_Transactions(db.Model):
    __tablename__ = "fp_transaction"

    id = db.Column(db.Integer, primary_key=True)
    manager_name = db.Column(db.String)
    season = db.Column(db.Integer)
    week = db.Column(db.String)
    payout_penalty = db.Column(db.String)
    transaction_value = db.Column(db.Float)
    transaction_type = db.Column(db.String)
    transaction_description = db.Column(db.String)

    def __init__(self, manager_name, season, week, payout_penalty, transaction_value, transaction_type, transaction_description):
        self.manager_name = manager_name
        self.season = season
        self.week = week
        self.payout_penalty = payout_penalty
        self.transaction_value = transaction_value
        self.transaction_type = transaction_type
        self.transaction_description = transaction_description


    def __repr__(self):
        return "<FP_Transaction: {} {} {} {} {} {} {}>".format(self.manager_name, self.season, self.week,
                                                      self.payout_penalty, self.transaction_value,
                                                      self.transaction_type, self.transaction_description)

class FP_Week_Start(db.Model):
    __tablename__ = "fp_week_start"

    id = db.Column(db.Integer, primary_key=True)
    starting_balance = db.Column(db.String)
    week1 = db.Column(db.Float)
    week2 = db.Column(db.Float)
    week3 = db.Column(db.Float)
    week4 = db.Column(db.Float)
    week5 = db.Column(db.Float)
    week6 = db.Column(db.Float)
    week7 = db.Column(db.Float)
    week8 = db.Column(db.Float)
    week9 = db.Column(db.Float)
    week10 = db.Column(db.Float)
    week11 = db.Column(db.Float)
    week12 = db.Column(db.Float)
    week13 = db.Column(db.Float)
    week14 = db.Column(db.Float)
    week15 = db.Column(db.Float)
    week16 = db.Column(db.Float)
    placeholder = db.Column(db.String)

    def __init__(self, starting_balance):
        self.starting_balance = starting_balance

    def __repr__(self):
        return "<FP_Totals: {}>".format(self.starting_balance)

class FP_Week_End(db.Model):
    __tablename__ = "fp_week_end"

    id = db.Column(db.Integer, primary_key=True)
    ending_balance = db.Column(db.String)
    week1 = db.Column(db.Float)
    week2 = db.Column(db.Float)
    week3 = db.Column(db.Float)
    week4 = db.Column(db.Float)
    week5 = db.Column(db.Float)
    week6 = db.Column(db.Float)
    week7 = db.Column(db.Float)
    week8 = db.Column(db.Float)
    week9 = db.Column(db.Float)
    week10 = db.Column(db.Float)
    week11 = db.Column(db.Float)
    week12 = db.Column(db.Float)
    week13 = db.Column(db.Float)
    week14 = db.Column(db.Float)
    week15 = db.Column(db.Float)
    week16 = db.Column(db.Float)
    placeholder = db.Column(db.String)

    def __init__(self, ending_balance):
        self.ending_balance = ending_balance

    def __repr__(self):
        return "<FP_Totals: {}>".format(self.ending_balance)

class Requests(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    request_name = db.Column(db.String)
    request_manager = db.Column(db.String)
    request_text = db.Column(db.String)
    request_status = db.Column(db.String)

    def __init__(self, request_name, request_manager, request_text, request_status):
        self.request_name = request_name
        self.request_manager = request_manager
        self.request_text = request_text
        self.request_status = request_status

    def __repr__(self):
        return "<Request: {}>".format(self.request_name_name)

class SideBets(db.Model):
    __tablename__ = "side_bets"

    id = db.Column(db.Integer, primary_key=True)
    manager_name1 = db.Column(db.String)
    manager_name2 = db.Column(db.String)
    bet_desc = db.Column(db.String)
    bet_amount = db.Column(db.String)
    manager1_approval = db.Column(db.String)
    manager2_approval = db.Column(db.String)
    season = db.Column(db.String)
    bet_outcome = db.Column(db.String)

    def __init__(self, manager_name1, manager_name2, bet_desc, bet_amount, manager1_approval, manager2_approval, season, bet_outcome):
        self.manager_name1 = manager_name1
        self.manager_name2 = manager_name2
        self.bet_desc = bet_desc
        self.bet_amount = bet_amount
        self.manager1_approval = manager1_approval
        self.manager2_approval = manager2_approval
        self.season = season
        self.bet_outcome = bet_outcome


    def __repr__(self):
        return "<Side Bets: {}>".format(self.bet_desc)

class Lifetime_Stats(db.Model):
    __tablename__ = "league_history_cumulative"

    index = db.Column(db.Integer, primary_key=True)
    record_overall_losses = db.Column(db.Integer)
    record_overall_pointsAgainst = db.Column(db.String)
    record_overall_pointsFor = db.Column(db.String)
    record_overall_wins = db.Column(db.String)
    manager = db.Column(db.String)

    def __init__(self, record_overall_losses, record_overall_pointsAgainst, record_overall_pointsFor,
                 record_overall_wins, manager):
        self.record_overall_losses = record_overall_losses
        self.record_overall_pointsAgainst = record_overall_pointsAgainst
        self.record_overall_pointsFor = record_overall_pointsFor
        self.record_overall_wins = record_overall_wins
        self.manager = manager

    def __repr__(self):
        return "<Lifetime Stats: {}>".format(self.manager)

    @classmethod
    def get_elements(cls):
        results = []
        query = db_session.query(Lifetime_Stats).order_by(desc(Lifetime_Stats.record_overall_pointsFor))
        results = query.all()
        return results

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, index):
        return [i for i in cls.get_elements() if i.index == index][0]

class Matchup_Stats(db.Model):
    __tablename__ = "matchup_stats"

    id = db.Column(db.Integer, primary_key=True)
    head_to_head_matchup = db.Column(db.String)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    tie = db.Column(db.Integer)
    points_for = db.Column(db.Integer)
    points_against = db.Column(db.Integer)

    def __init__(self, head_to_head_matchup, wins, losses, tie, points_for, points_against):
        self.head_to_head_matchup = head_to_head_matchup
        self.wins = wins
        self.losses = losses
        self.tie = tie
        self.points_for = points_for
        self.points_against = points_against

    def __repr__(self):
        return "<Lifetime Stats: {}>".format(self.head_to_head_matchup)

    @classmethod
    def get_elements(cls):
        results = []
        query = db_session.query(Matchup_Stats)
        results = query.all()
        return results

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, index):
        return [i for i in cls.get_elements() if i.index == index][0]