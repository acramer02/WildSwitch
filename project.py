import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

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
        x = db.execute("SELECT COUNT(*) AS 'count' FROM users WHERE username = ?", request.form.get("username"))

        # if username already in users table, return apology message 
        if 0 != x[0]["count"]:
            return apology("Username Taken")
        
        # checks if password and confirmation match, return apology if don't
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")

        # hash password
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # if passes all the checks, add username+hash to users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        
        # return users info for now registered user by searching for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # log user into session by id
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # TODO
    # SELECT all info FROM cards WHERE users.id = session["user_id"]
    ## Update this when we actually have the right data tables
    ## stocks_table = db.execute("SELECT symbol AS 'symbols' FROM portfolio WHERE user_id=?", session["user_id"])
    ## stocks_list = []

    # TODO
    # sum the current value of every card the user owns
    # total = db.execute("SELECT SUM(stock_total) AS 'sum' FROM portfolio WHERE user_id = ?", session["user_id"])

    # prevents error when no stocks are owned by setting total stock value to $0
    if total[0]['sum'] is None:
        total[0]['sum'] = 0
    
    # TODO
    # gets current amount of cash for user
    # cash = db.execute("SELECT cash AS 'cash' FROM users WHERE id = ?", session["user_id"])
    # calculates user's current cash owned plus current value of all stock owned
    # total_value = total[0]['sum'] + cash[0]['cash']

    # passes portfolio for user, current cash, and total_value of stocks+cash to index.html for display
    # return render_template("index.html", portfolio=portfolio, cash=usd(cash[0]['cash']), value=usd(total_value))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # if symbol doesn't exist or isn't real, and if share isn't whole number >= 1
        if lookup(request.form.get("symbol")) is None:
            return apology("Invalid Symbol")
        if request.form.get("shares") == "":
            return apology("Please enter shares.")
        if not request.form.get("shares").isnumeric():
            return apology("Please enter valid shares value.")
        if float(request.form.get("shares")) < 1:
            return apology("Please enter valid shares value.")

        # gets info about stock trying to buy
        stock = lookup(request.form.get("symbol"))
        name = stock["name"]
        symbol = stock["symbol"]
        price = stock["price"]

        # gets user's current cash amount, shares trying to buy, and the total cost of purchase
        user_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        shares = request.form.get("shares")
        total_cost = float(shares) * float(price)

        # makes sure total cost is less than or equal to amount of cash in account (can afford)
        if total_cost > user_cash[0]["cash"]:
            return apology("Can't afford.")

        # update user's cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash[0]["cash"] - total_cost, session["user_id"])

        # gets time of transaction https://www.w3resource.com/python-exercises/python-basic-exercise-3.php for the current time
        e = datetime.datetime.now()
        now = e.strftime("%Y-%m-%d %H:%M:%S")

        # add transaction to table
        db.execute("INSERT INTO transactions (symbol, shares, price, time, user_id) VALUES (?, ?, ?, ?, ?)", 
                   symbol, shares, usd(price), now, session["user_id"])

        # gets frequency of symbol in user's portfolio (1 if exist, 0 if not)
        exist = db.execute("SELECT COUNT(*) AS 'count' FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        # if user doesn't already own the stock, add purchase into portfolio
        if exist[0]["count"] == 0:
            db.execute("INSERT INTO portfolio (symbol, name, shares, price, stock_total, user_id) VALUES (?, ?, ?, ?, ?, ?)", 
                       symbol, name, shares, usd(price), total_cost, session["user_id"])
            return redirect("/")
        # if user already owns the stock, upate share count
        else:
            old_shares = db.execute("SELECT shares AS 'shares' FROM portfolio WHERE user_id=? AND symbol=?", 
                                    session["user_id"], symbol)
            new_shares = float(old_shares[0]['shares']) + float(shares)
            db.execute("UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?", new_shares, session["user_id"], symbol)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # when they click on sell button
    if request.method == "POST":

        # check that user inputs symbol and shares
        if request.form.get("symbol") is None:
            return apology("Missing symbol.")
        if request.form.get("shares") == "":
            return apology("Missing Shares.")

        # get stock information for requested stock
        stock = lookup(request.form.get("symbol"))
        name = stock["name"]
        symbol = stock["symbol"]
        price = stock["price"]

        # sets shares variable equal to user input 
        shares = -1 * int(request.form.get("shares"))
        # gets old amount of shares from portfolio
        old_shares = db.execute("SELECT shares AS 'shares' FROM portfolio WHERE user_id=? AND symbol=?", session["user_id"], symbol)
        # sets new value for shares equal to old - new (addition because we already made shares negative)
        new_shares = float(old_shares[0]['shares']) + float(shares)

        # make sure that they can't sell more shares than they have
        if new_shares < 0:
            return apology("Too many shares.")
        # if they sell all, delete from portfolio
        elif new_shares == 0:
            db.execute("DELETE FROM portfolio WHERE symbol=? AND user_id=?", symbol, session["user_id"])

        # how much money you get from sale
        total_value = float(shares) * float(price)
        
        # get user's pre-sale cash from users
        user_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # update cash to be pre-sale + sale windfall
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash[0]["cash"] - total_value, session["user_id"])
        
        # credit to this website for how to get date and time
        # https://www.w3resource.com/python-exercises/python-basic-exercise-3.php for the current time
        e = datetime.datetime.now()
        now = e.strftime("%Y-%m-%d %H:%M:%S")

        # insert this new transaction into transactions table
        db.execute("INSERT INTO transactions (symbol, shares, price, time, user_id) VALUES (?, ?, ?, ?, ?)", 
                   symbol, shares, usd(price), now, session["user_id"])
        # update portfolio to reflect new amount of shares
        db.execute("UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?", new_shares, session["user_id"], symbol)
        
        # take user to index
        return redirect("/")
    
    # when they visit the page, portfolio reflects the stocks they own
    else:
        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", portfolio=portfolio)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # creates a table of all the current user's transactions
    transactions = db.execute("SELECT * FROM transactions WHERE user_id=?", session["user_id"])

    # passes transactions table into html
    return render_template("history.html", transactions=transactions)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)