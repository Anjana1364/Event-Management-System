from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# create db table
db = sqlite3.connect("database.db")
db.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)")
db.commit()
db.close()

# sample events
events = [
    (1, "UI/UX Bootcamp", "Jan 2, 2026", "Chennai"),
    (2, "Python Meetup", "Jan 8, 2026", "Bangalore"),
    (3, "Startup Meet", "Jan 18, 2026", "Hyderabad")
]

@app.route("/", methods=["GET","POST"])
def login():
    msg = ""
    if request.method == "POST":
        e = request.form["email"]
        p = request.form["password"]

        db = sqlite3.connect("database.db")
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",(e,p)
        ).fetchone()
        db.close()

        if user:
            return redirect("/success")
        msg = "Wrong login"

    return render_template("login.html", message=msg, events=events)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        db = sqlite3.connect("database.db")
        db.execute(
            "INSERT INTO users VALUES (?,?)",
            (request.form["email"], request.form["password"])
        )
        db.commit()
        db.close()
        return redirect("/")
    return render_template("register.html")

@app.route("/event/<int:id>")
def event(id):
    return render_template("event_register.html", event=events[id-1])

@app.route("/success")
def success():
    return render_template("success.html")

app.run(debug=True)
