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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)


class TodosTable(db.Model):
    """
    users todo information.
    
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

@app.route("/",methods=['GET', 'POST']) #get
def signInPage():
    '''
    Home page    
    '''  

   # userExists= db.session.query(UsersTable.id).filter_by(username)    
    if request.method == "POST" and request.form['username']:
        
        enteredusername = request.form["username"]
        enteredpassword = request.form["password"]
        existinguser = db.session.query(UsersTable).filter_by(username = enteredusername).first()
               
        try:
            if enteredusername == existinguser.username:
                print("User found ")
                print(existinguser.username)
                
                if enteredpassword == existinguser.password:
                    print('password matches')
                    return redirect(url_for("todoList"))  
                else:
                    print('password does not match')
        except AttributeError:
            print("User not found")          
            return render_template('signInPage.html')
        
    return render_template('signInPage.html')

    

@app.route("/makeAccount", methods=['GET',  'POST']) 
def makeAccount():
    """
    Make Account
    """        
    if request.method == "POST" and request.form['password'] == request.form['cpassword']:
        
        newuser = UsersTable(request.form['username'],request.form['password'])
        db.session.add(newuser)
        db.session.commit()

        print('Account created')
        return redirect(url_for("signInPage"))
    else:
        print('User name not entered')
        
    return render_template('makeAccount.html')

@app.route("/todoList", methods =['GET', 'POST'])
def todoList():
    """
    Todo List
    """
    
    if request.method == 'POST' and request.form['signout']:
                
        return redirect(url_for("signInPage"))

    return render_template('todoList.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
