from enum import unique
from operator import methodcaller
from flask import Flask, redirect, url_for, render_template, request
from flask.helpers import flash
from flask.signals import request_finished
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.operators import exists
from wtforms import Form, BooleanField,StringField,PasswordField,validators
from flask_wtf import FlaskForm

#DATABASE =  

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Richi/Desktop/flask_project/user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)



class TodosTable(db.Model):
    """
    users todo information. I believe that I will have to make a relationship between the tables. 
    
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique = True,nullable = False)
    task = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

class UsersTable(db.Model):
    """
    This is going to be where user data is interacted with 
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique = True,nullable = False)
    password = db.Column(db.String(20), unique = False,nullable = False)
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return "user: {} password : {}".format(self.username,self.password)