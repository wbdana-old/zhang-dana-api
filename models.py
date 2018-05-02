from app import db
from sqlalchemy.dialects.postgresql import JSON

class Rsvp(db.Model):
    __tablename__ = 'rsvps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    rehearsal = db.Column(db.Boolean())
    wedding = db.Column(db.Boolean())
    brunch = db.Column(db.Boolean())

    def __init__(self, name, email, rehearsal, wedding, brunch):
        self.name = name
        self.email = email
        self.rehearsal = rehearsal
        self.wedding = wedding
        self.brunch = brunch

    def __repr__(self):
        return '<id {} name {} email {} rehearsal {} wedding {} brunch {}>'.format(self.id, self.name, self.email, self.rehearsal, self.wedding, self.brunch)
