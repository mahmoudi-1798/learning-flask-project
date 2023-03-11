# in this part we want to 

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

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
db = SQLAlchemy(app) 

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.before_first_request
def create_tables():
     db.create_all()


# if the route is "sth" render sth
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


# for login we use request methods like POST and GET
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()


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
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved !")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in. Please login first !", "info")
        return redirect(url_for("login"))


@app.route("/delete")
def delete():
    user = session["user"]
    logout()
    dl_user = users.query.filter_by(name=user).first()
    if dl_user:
        db.session.delete(dl_user)
        db.session.commit()
    else:
        flash("You have nothing to delete !", "info")


    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


""" - Create a sign in page and signing functionality """