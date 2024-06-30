from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from src.utils import *
import json
from flask_jsglue import JSGlue

SESSION_TYPE = 'memcache'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yash/Desktop/exams_app/mcq_project/database.db'
db = SQLAlchemy(app)
jsglue = JSGlue()
jsglue.init_app(app)

app.secret_key = "quiz_app"  

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def index():
    session['login'] = 0
    return render_template("home.html")



@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            session['login'] = 1
            session['username'] = uname
            return redirect(url_for("instructions"))
    return render_template("login.html")

@app.route("/logout",methods=["GET", "POST"])
def logout():
    session['username'] = None
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/instructions", methods=["GET", "POST"])
def instructions():
    ####start timer on exam start#####
    # if request.method == "POST":
    return render_template("instructions.html",name = session['username'])


@app.route("/startexam", methods=["GET", "POST"])
def startexam():
    ####start timer on exam start#####
    # if request.method == "POST":
    # session['ques_length'] ,session['questions']  = generate_questions(5)
    # session['answers'] = []
    i,que_index,questions = generate_questions(2)
    print ("questions",questions)
    ###generate correct answer list from questions#####
    return render_template("startexam.html", question = questions)



@app.route("/submit", methods=["GET", "POST"])
def submit():
    ####start timer on exam start#####
    if request.method == "POST":
        content = request.get_data()
        print ("conetnt",content)
        return render_template("result.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    ####start timer on exam start#####
    # if request.method == "POST":
    return render_template("result.html")


if __name__ == "__main__":
    db.create_all()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.debug = True
    app.run(debug=True)