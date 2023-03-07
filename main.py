# in this part we want to 

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import sqlalchemy

#importing libraries needed 
    # flask
    # redirect to redirect a specific url to other
    # url_for to use for redirect to a page
    # render_template to show a html file
    # request for login request methods
    # seession to store a data in browser
    # flash to show sth likw alert 
    # sqlachemy to srore some of user data in db

app = Flask(__name__)
# declare sth in biggining
app.secret_key = "hell"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["AQLALCHEMY_TRICK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

# initiallize the data base
db = sqlalchemy(app) 

class users(db.model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


# if the route is "sth" render sth
@app.route("/")
def home():
    return render_template("index.html")


# for login we use request methods like POST and GET
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash(f"{user}  have logged in!", "info")
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged in !", "info")
            return redirect(url_for("user"))
        
        return render_template("login.html")


@app.route("/logout")
def logout():
    # to show a message to user
    if "user" in session:
        user = session["user"]
        flash(f"{user}  have been logged out!", "info")
        session.pop("user", None)
        session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved !")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in. Please login first !", "info")
        return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)