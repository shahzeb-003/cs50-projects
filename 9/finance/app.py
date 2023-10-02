import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""

    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as shares, operation FROM stocks WHERE userID = ? GROUP BY symbol HAVING (SUM(shares)) > 0;",
        session["user_id"],
    )
    total_cash_stocks = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["shares"]
        total_cash_stocks = total_cash_stocks + stock["total"]

    total_cash = total_cash_stocks + user_cash[0]["cash"]
    return render_template(
        "index.html", stocks=stocks, user_cash=user_cash[0], total_cash=total_cash
    )



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        noshares = request.form.get("shares")
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        cash = db.execute("SELECT cash FROM users where id = ?", session["user_id"])[0]["cash"]

        if quote is None:
            return apology("must provide valid symbol", 400)
        elif not symbol:
            return apology("must be valid symbol", 400)

        try:
            noshares = int(noshares)
            if noshares < 1:
                return apology("share must be a positive integer", 400)
        except ValueError:
            return apology("share must be a positive integer", 400)

        shares_price = noshares * quote["price"]
        if cash < (shares_price):
            return apology("cash is not sufficient", 400)

        else:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", shares_price, session["user_id"])
            db.execute("INSERT INTO stocks (userID, symbol, shares, price, operation) VALUES (?, ?, ?, ?, ?)", session["user_id"], symbol.upper(), noshares, quote["price"], "buy")

        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT * FROM stocks WHERE userID = ?", session["user_id"])
    return render_template("history.html", stocks=stocks)


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
    """Get stock quote."""

    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))

        if quote is None:
            return apology("must provide valid symbol", 400)
        else:
            return render_template(
                "quoted.html",
                name=quote["name"],
                symbol=quote["symbol"],
                price=quote["price"],
            )
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
     if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure the username was submitted
        if not username:
            return apology("must provide username", 400)
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide a confirmation password", 400)

        # Ensure passwords match
        elif not password == confirmation:
            return apology("passwords must match", 400)

        else:
            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?) ", username, hash,
            )
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
     else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        noshares = request.form.get("shares")
        user_shares = db.execute("SELECT SUM(shares) as shares FROM stocks where userID = ? AND symbol = ?", session["user_id"], symbol.upper())[0]

        if quote is None:
            return apology("must provide valid symbol", 400)
        elif not symbol:
            return apology("must be valid symbol", 400)
        elif int(noshares) > user_shares["shares"]:
            return apology("you don't have that many shares", 400)

        try:
            noshares = int(noshares)
            if noshares < 1:
                return apology("share must be a positive integer", 400)
        except ValueError:
            return apology("share must be a positive integer", 400)

        shares_price = noshares * quote["price"]


        db.execute(
            "INSERT INTO stocks (userID, symbol, shares, price, operation) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            symbol.upper(),
            -noshares,
            quote["price"],
            "sell",
        )

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            shares_price,
            session["user_id"],
        )

        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol FROM stocks WHERE userID = ? GROUP BY symbol",
            session["user_id"],
        )
        return render_template("sell.html", stocks=stocks)
