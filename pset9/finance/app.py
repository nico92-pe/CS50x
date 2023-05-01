import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
import time
from tempfile import mkdtemp
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
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    db_userid = session.get("user_id")
    trades = db.execute(
        "SELECT * FROM (SELECT symbol, name, SUM(shares) as shares, price, total FROM history WHERE user=? GROUP by symbol) WHERE shares>0", db_userid)
    query = db.execute("SELECT cash FROM users WHERE id=?", db_userid)
    db_cash = query[0]["cash"]
    counter = 0
    invested = 0

    for i in trades:
        symbol = trades[counter]["symbol"]
        symbol_quote = lookup(symbol)
        price = symbol_quote["price"]

        trades[counter]["price"] = price
        trades[counter]["total"] = price * trades[counter]["shares"]
        invested = invested + trades[counter]["total"]

        counter = counter+1
    total = invested + db_cash
    return render_template("home.html", trades=trades, cash=db_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        # Check if the user input a Symbol
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)

        # Check if the user input the number of shares
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)

        if not request.form.get("shares").isdigit():
            return apology("INPUT POSITIVE NUMBER", 400)

        # Save the input and get the quote
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        symbol_quote = lookup(symbol)

        # Check if the symbol exists
        if symbol_quote == None:
            return apology("INVALID SYMBOL", 400)

        db_price = symbol_quote["price"]
        db_symbol = symbol_quote["symbol"]
        db_name = symbol_quote["name"]
        db_total = db_price * int(shares)
        db_userid = session.get("user_id")

        timestamp = time.time()
        # convert to datetime
        date_time = datetime.fromtimestamp(timestamp)

        # convert timestamp to string in dd-mm-yyyy HH:MM:SS
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")

        query = db.execute("SELECT cash FROM users WHERE id=?", db_userid)
        db_cash = query[0]["cash"]

        if db_total < db_cash:
            db_newcash = db_cash - db_total
            db.execute("UPDATE users SET cash= ? WHERE id=?", db_newcash, db_userid)
            db.execute("INSERT INTO history (symbol, name, shares, price, total, timestamp, user) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       db_symbol, db_name, shares, db_price, db_total, str_date_time, db_userid)
            return redirect("/")
        return apology("CAN'T AFFORD", 400)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    db_userid = session.get("user_id")
    trades = db.execute("SELECT * FROM history WHERE user=?", db_userid)
    return render_template("history.html", trades=trades)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol_quote = lookup(symbol)
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)
        if symbol_quote == None:
            return apology("INVALID SYMBOL", 400)
        else:
            return render_template("quoted.html", quoted=symbol_quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if username == "" or password == "" or password == "":
            return apology("missing username and/or passowrd", 400)
        elif len(rows) == 1:
            return apology("username already exists", 400)
        elif password != password2:
            return apology("passwords are not the same", 400)
        else:
            hash_pass = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_pass)
            # Remember which user has logged in
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        db_shares = shares * -1
        db_userid = session.get("user_id")

        symbol_quote = lookup(symbol)
        db_price = symbol_quote["price"]
        db_symbol = symbol_quote["symbol"]
        db_name = symbol_quote["name"]
        db_total = db_price * shares
        query_cash = db.execute("SELECT cash FROM users WHERE id=?", db_userid)

        db_cash = query_cash[0]["cash"]
        print(db_cash)

        timestamp = time.time()
        print(timestamp)
        # convert to datetime
        date_time = datetime.fromtimestamp(timestamp)

        # convert timestamp to string in dd-mm-yyyy HH:MM:SS
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")

        query = db.execute("SELECT shares FROM history WHERE user=? AND symbol=?", db_userid, symbol)
        sell_shares = 0
        i = 0
        for a in query:
            sell_shares = sell_shares + query[i]["shares"]
            i = i+1

        if shares <= sell_shares:
            db.execute("INSERT INTO history (symbol, name, shares, price, total, timestamp, user) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       db_symbol, db_name, db_shares, db_price, db_total, str_date_time, db_userid)
            db_newcash = db_cash + db_total
            db.execute("UPDATE users SET cash= ? WHERE id=?", db_newcash, db_userid)
            return redirect("/")
        else:
            return apology("TOO MANY SHARES", 400)

    else:
        db_userid = session.get("user_id")
        trades = db.execute("SELECT symbol FROM history WHERE user=?", db_userid)
        result = list(
            {
                dictionary['symbol']: dictionary
                for dictionary in trades
            }.values()
        )
        return render_template("sell.html", result=result)