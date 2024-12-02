from app.db import db
from enum import Enum

class UserType(Enum):
    USER = 1
    MANAGER = 2

user_shift = db.Table('user_shift',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('shift_id', db.Integer, db.ForeignKey('shift.id'), primary_key=True)
)

class User(db.Model):
    # Required for flask-login
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False)
    is_anonymous = db.Column(db.Boolean, nullable=False)
    is_authenticated = db.Column(db.Boolean, nullable=False)
    def get_id(self):
        return str(self.id)
    # Other Properties
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.Integer, nullable=False)
    shifts = db.relationship("Shift", secondary=user_shift, back_populates="workers")
    unavailability = db.relationship("Unavailability", backref="user", lazy="dynamic")
    @property
    def name(self):
        return f"{self.fname} {self.lname}"
    

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    workers_required = db.Column(db.Integer, nullable=False)
    workers = db.relationship("User", secondary=user_shift, back_populates="shifts")
    creating_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    creating_user = db.relationship("User", backref="created_shifts", foreign_keys=[creating_user_id])

class Unavailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))