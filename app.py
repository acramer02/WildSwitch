import os, csv
import datetime
import sqlite3
import jinja2

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, generate_card, generate_user, usd, build_market

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# opens connection to database
con = sqlite3.connect("wildswitch.sqlite", check_same_thread=False)
cur = con.cursor()



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

         cur.execute("SELECT cash FROM Users WHERE username = ?", (session["user_id"],))
         cash = int(cur.fetchone()[0])

         player = int(request.form.get("buy"))

         cur.execute("SELECT * FROM Market")
         players = list(cur.fetchall())
         selected = players[player]

         if selected[5] > cash:
             return apology("Can't afford - please add money to account.")
         elif selected[4] == 1:
             return apology("Already purchased!")
         else:
             # adds bought card into cards table
             cur.execute("INSERT INTO Cards (username, playerID, cardValue, status, position, year) VALUES (?, ?, ?, ?, ?, ?)", (session["user_id"], selected[0], selected[5], '0', selected[3], selected[2],))
             # subtracts card cost from users total cash supply
             cur.execute("UPDATE Users SET cash = cash - ? WHERE username = ?", (selected[5], session["user_id"],))
             # updates status in market to mean bought
             cur.execute("UPDATE Market SET status = '1' WHERE playerID = ?", (selected[0],))

             # updates status to mean owned for whichever table the card resides in
             if selected[3] == 1:
                 cur.execute("UPDATE Batting SET status = '1' WHERE playerID = ? AND yearID = ?", (selected[0], selected[2]))
             else:
                 cur.execute("UPDATE Pitching SET status = '1' WHERE playerID = ? AND yearID = ?", (selected[0], selected[2]))
             con.commit()

             return redirect("/mycards")

    else:
        batters = []
        pitchers = []

        cur.execute("SELECT playerID, year, position FROM Market")
        market = list(cur.fetchall())

        for i in range(len(market)):
            if market[i][2] == 1:
                cur.execute("SELECT * FROM Batting WHERE playerID = ? AND yearID = ?", (market[i][0], market[i][1],))
                batters.append(cur.fetchone())
            else:
                cur.execute("SELECT * FROM Pitching WHERE playerID = ? AND yearID = ?", (market[i][0], market[i][1],))
                pitchers.append(cur.fetchone())

        return render_template("buy.html", batters=batters, pitchers=pitchers)

@app.route("/mycards", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":
        if request.form['name'] == 'sell':
            # Ensure player name was submitted
            if not request.form.get("playername"):
                return apology("Must provide player name.", 403)

            # Ensure year was submitted
            elif not request.form.get("year"):
                return apology("Must provide year.", 403)

            # Check if card exists with their username, playername, and year
            cur.execute("SELECT COUNT(playerID) FROM Cards WHERE username = ? AND fullName = ? AND yearID = ?", (session["user_id"], request.form.get("playersell"), request.form.get("yearsell")))
            if int(cur.fetchone()[0]) == 0:
                return apology("You do not own this card.")

            #Get value of card
            cur.execute("SELECT cardValue FROM cards WHERE username = ? AND fullName = ? AND yearID = ?", (session["user_id"], request.form.get("playersell"), request.form.get("yearsell"))) 
            value = cur.fetchone()[0]

            #Get user's old cash
            cur.execute("SELECT cash FROM Users WHERE username = ?", session["user_id"])
            cash = cur.fetchone()[0]

            #Update user's cash
            cur.execute("UPDATE Users SET cash = ? WHERE username = ?", cash + value, session["user_id"])

            #Delte card from cards
            cur.execute("DELETE FROM Cards WHERE username = ? AND fullName = ? AND yearID = ?", (session["user_id"], request.form.get("playersell"), request.form.get("yearsell")))
            con.commit()

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            batters = []
            pitchers = []

            cur.execute("SELECT playerID, year FROM Cards WHERE username = ? AND position = 1", (session["user_id"],))
            batterInfo = list(cur.fetchall())

            cur.execute("SELECT playerID, year FROM Cards WHERE username = ? AND position = 0", (session["user_id"],))
            pitcherInfo = list(cur.fetchall())

            for i in range(len(batterInfo)):
                cur.execute("SELECT * FROM Batting WHERE playerID = ? AND yearID = ?", (batterInfo[i][0], batterInfo[i][1],))
                batters.append(list(cur.fetchall()))

            
            for i in range(len(pitcherInfo)):
                cur.execute("SELECT * FROM Pitching WHERE playerID = ? AND yearID = ?", (pitcherInfo[i][0], pitcherInfo[i][1],))
                pitchers.append(list(cur.fetchall()))

            cur.execute("SELECT cash FROM Users WHERE username = ?", (session["user_id"],))
            cash = int(cur.fetchone()[0])

            cur.execute("SELECT COUNT(*) FROM Cards WHERE username = ?", (session["user_id"],))
            cardCount = int(cur.fetchone()[0])
            
            return render_template("mycards.html", batters=batters, pitchers=pitchers, cash=cash, cardCount=cardCount, username=session["user_id"])


@app.route("/mycards", methods=["GET", "POST"])
@login_required
def mycards():

    if request.method == "POST":
         
         cur.execute("UPDATE Users SET cash = ? WHERE username = ?", )
    else:
        batters = []
        pitchers = []

        cur.execute("SELECT playerID, year FROM Cards WHERE username = ? AND position = 1", (session["user_id"],))
        batterInfo = list(cur.fetchall())

        cur.execute("SELECT playerID, year FROM Cards WHERE username = ? AND position = 0", (session["user_id"],))
        pitcherInfo = list(cur.fetchall())

        for i in range(len(batterInfo)):
            cur.execute("SELECT * FROM Batting WHERE playerID = ? AND yearID = ?", (batterInfo[i][0], batterInfo[i][1],))
            batters.append(list(cur.fetchall()))

        
        for i in range(len(pitcherInfo)):
            cur.execute("SELECT * FROM Pitching WHERE playerID = ? AND yearID = ?", (pitcherInfo[i][0], pitcherInfo[i][1],))
            pitchers.append(list(cur.fetchall()))

        cur.execute("SELECT cash FROM Users WHERE username = ?", (session["user_id"],))
        cash = int(cur.fetchone()[0])

        cur.execute("SELECT COUNT(*) FROM Cards WHERE username = ?", (session["user_id"],))
        cardCount = int(cur.fetchone()[0])
        
        return render_template("mycards.html", batters=batters, pitchers=pitchers, cash=cash, cardCount=cardCount, username=session["user_id"])

@app.route("/")
@login_required
def index():
    
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    
    if request.method == "POST":
        search = request.form.get("search")
        option = int(request.form.get("criteria"))

        if option == 1:
            cur.execute("SELECT COUNT(*) FROM Batting WHERE LOWER(fullName) LIKE LOWER(?)", (search,))
            count = float(cur.fetchone()[0])

            if count != 0.0:
                cur.execute("SELECT playerID FROM Batting WHERE LOWER(fullName) LIKE LOWER(?)", (search,))
                playerID = cur.fetchone()[0]
                return generate_card(playerID, 1)
            else:
                return apology("Not a valid player name.")

        elif option == 2:
            cur.execute("SELECT COUNT(*) FROM Pitching WHERE LOWER(fullName) LIKE LOWER(?)", (search,))
            count = float(cur.fetchone()[0])

            if count != 0.0:
                cur.execute("SELECT playerID FROM Pitching WHERE LOWER(fullName) LIKE LOWER(?)", (search,))
                playerID = cur.fetchone()[0]
                return generate_card(playerID, 0)
            else:
                return apology("Not a valid player name.")
        else:
            cur.execute("SELECT COUNT(*) FROM Users WHERE LOWER(username) LIKE LOWER(?)", (search,))
            count = float(cur.fetchone()[0])

            if count != 0.0:
                cur.execute("SELECT username FROM Users WHERE LOWER(username) LIKE LOWER(?)", (search,))
                username = cur.fetchone()[0]

                return generate_user(username)
            else:
                return apology("Not a valid player name.")
    else:
        return render_template("search.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.", 403)

        # Query database for username
        cur.execute("SELECT * FROM Users WHERE username = ?", (request.form.get("username"),))
        rows = list(cur.fetchall())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][1]

        # generates market
        build_market()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    # when register button is clicked
    if request.method == "POST":

        # checks that all forms have valid input
        if not request.form.get("username"):
            return apology("Please enter username.")
        elif not request.form.get("password"):
            return apology("Please enter password.")
        elif not request.form.get("confirmation"):
            return apology("Please enter confirmation.")

        # checks if username is already in users table, stores 1 if found, 0 if not
        cur.execute("SELECT COUNT(*) AS 'count' FROM Users WHERE username = ?", (request.form.get("username"),))
        count = float(cur.fetchone()[0])

        # if username already in users table, return apology message 
        if 0.0 != count:
            return apology("Username taken.")
        
        # checks if password and confirmation match, return apology if don't
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")

        # hash password
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # if passes all the checks, add username+hash to users table
        cur.execute("INSERT INTO Users (username, password, cash) VALUES (?, ?, 50.00)", (request.form.get("username"), hash,))
        con.commit()

        # return users info for now registered user by searching for username
        cur.execute("SELECT * FROM Users WHERE username = ?", (request.form.get("username"),))
        rows = list(cur.fetchall())

        # log user into session by id
        session["user_id"] = rows[0][1]

        # generates market
        build_market()

        # redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")
