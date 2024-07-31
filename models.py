from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)


class user(db.Model):
    __tablename__ = user
    type = db.column(db.String(1), nullable = False)
    name = db.column(db.String(20), unique= True, primary_key = True, nullable = False)
    password = db.column(db.String(20), nullable= False)

class 

class campaign(db.Model):
    __tablename__ = campaign
    sponsor = db.column(db.String(20),db.ForeignKey('user.name'),nullable=False)
    campaign_name= db.column(db.String(64),primary_key=True, nullable =False, )