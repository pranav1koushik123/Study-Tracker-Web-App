from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()
#--------User Table----------#
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
#----------Study session table----#
class Sessions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date=db.Column(db.String(100),nullable=False)
    hours=db.Column(db.String(100),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    subjects_id=db.Column(db.Integer,db.ForeignKey('subjects.id'))
#------subjects table-------#
class Subjects(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True,nullable=False)
    description=db.Column(db.String(100))
    session=db.relationship('Sessions',backref='subjects',lazy=True)
