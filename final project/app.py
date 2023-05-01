from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cambia.db")

# Super_admin
    # username = super_admin
    # password = Andrea1711*

@app.route("/")
@login_required
def index():

    return redirect("/clientes")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = 'falta username'
            return render_template("error.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = 'falta password'
            return render_template("error.html", error=error)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error = 'user/password errados'
            return render_template("error.html", error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Remember the user type
        session["user_type"] = rows[0]["type"]

        # Remember the user type
        session["sales_name"] = rows[0]["name"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():

    if request.method == "POST":
        return redirect("/usuarios-create")

    else:
        users = db.execute("SELECT * FROM users")
        return render_template("users.html", users=users)

@app.route("/usuarios-create", methods=["GET", "POST"])
@login_required
def usuarios_create():

    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("user"))

        # Validate if username exists
        if len(rows) == 1:
            error = 'Usuario ya existe.'
            page = 'usuarios-create'
            return render_template("error.html", error=error, page=page)

        # Validate the obligatory fields are filled
        if not request.form.get("name") or not request.form.get("phone") or not request.form.get("email") or not request.form.get("banco") or not request.form.get("account") or not request.form.get("birthday") or not request.form.get("user") or not request.form.get("user_type"):
            error = 'Faltan datos.'
            page = 'usuarios-create'
            return render_template("error.html", error=error, page=page)

        else:
            # Save the variables
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            bank = request.form.get("banco")
            account = request.form.get("account")
            birthday = request.form.get("birthday")
            user = request.form.get("user")
            user_type = db.execute("SELECT id FROM user_type WHERE name=?", request.form.get("user_type"))
            password = "cambia"
            hash_pass = generate_password_hash(password)

            # Insert to the DB
            db.execute("INSERT INTO users (name, phone, email, bank, bank_account, birthday, username, type, hash) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       name, phone, email, bank, account, birthday, user, user_type[0]["id"], hash_pass)
            return redirect("/usuarios")

    else:
        banks = db.execute("SELECT * FROM banks")
        user_types = db.execute("SELECT * FROM user_type")
        return render_template("users_new.html", banks=banks, user_types=user_types)

@app.route('/users_edit/<user>', methods=["GET", "POST"])
@login_required
def users_edit(user):

    if request.method == "POST":
        # Validate the obligatory fields are filled
        if not request.form.get("name") or not request.form.get("phone") or not request.form.get("email") or not request.form.get("banco") or not request.form.get("account") or not request.form.get("birthday"):
            error = 'Faltan datos.'
            page = 'usuarios'
            return render_template("error.html", error=error, page=page)

        else:
            # Save the variables
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            bank = request.form.get("banco")
            account = request.form.get("account")
            birthday = request.form.get("birthday")
            print(user)

            # Update the DB
            #db.execute("UPDATE users SET name=?, phone=?, email=?, bank=?, bank_account=?, birthday=?, WHERE id=?", name, phone, email, bank, account, birthday, user)
            db.execute("UPDATE users SET name=?, phone=?, email=?, bank=?, bank_account=?, birthday=? WHERE id=?", name, phone, email, bank, account, birthday, user)
            return redirect("/usuarios")

    else:
        banks = db.execute("SELECT * FROM banks")
        users = db.execute("SELECT * FROM users WHERE id=?", user)
        user_types = db.execute("SELECT user_type.name FROM user_type JOIN users ON user_type.id = users.type WHERE users.id=?", user)
        return render_template("users_edit.html", users=users, user=user, user_types=user_types, banks=banks)

@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clients():

    if request.method == "POST":
        return redirect("/clients-create")

    else:
        clients = db.execute("SELECT clients.id AS id, clients.name AS name, contact1_name, contact1_phone, address, district, users.name AS salesman, clients.salesman AS salesman_id FROM clients JOIN users ON clients.salesman = users.id;")
        return render_template("clients.html", clients=clients)

@app.route("/clients-create", methods=["GET", "POST"])
@login_required
def clients_create():

    if request.method == "POST":
        # Validate the obligatory fields are filled
        if not request.form.get("ruc") or not request.form.get("razon_social") or not request.form.get("name") or not request.form.get("salesman") or not request.form.get("contact1_name") or not request.form.get("contact1_phone") or not request.form.get("email") or not request.form.get("address") or not request.form.get("district") or not request.form.get("province"):
            error = 'Faltan datos.'
            page = 'clients-create'
            return render_template("error.html", error=error, page=page)
        else:
            # Save the variables
            ruc = request.form.get("ruc")
            razon_social = request.form.get("razon_social")
            name = request.form.get("name")
            salesman = request.form.get("salesman")
            data = db.execute("SELECT id FROM users WHERE name = ?", salesman)
            sales_id = data[0]["id"]
            contact1_name = request.form.get("contact1_name")
            contact1_phone = request.form.get("contact1_phone")
            contact2_name = request.form.get("contact2_name")
            contact2_phone = request.form.get("contact2_phone")
            email = request.form.get("email")
            address = request.form.get("address")
            district = request.form.get("district")
            province = request.form.get("province")

            # Insert to the DB
            db.execute("INSERT INTO clients (ruc, razon_social, name, salesman, contact1_name, contact1_phone, contact2_name, contact2_phone, email, address, district, province) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ruc, razon_social, name, sales_id, contact1_name, contact1_phone, contact2_name, contact2_phone, email, address, district, province)
            return redirect("/clientes")

    else:
        salesmen = db.execute("SELECT username, users.name AS name FROM users JOIN user_type ON users.type = user_type.id AND users.type=3")
        districts = db.execute("SELECT * FROM districts")
        provinces = db.execute("SELECT * FROM provinces")
        print(salesmen)
        return render_template("clients_new.html", salesmen=salesmen, districts=districts, provinces=provinces)

@app.route('/clients_edit/<client>', methods=["GET", "POST"])
@login_required
def clients_edit(client):

    if request.method == "POST":
        # Validate the obligatory fields are filled
        if not request.form.get("ruc") or not request.form.get("razon_social") or not request.form.get("name") or not request.form.get("salesman") or not request.form.get("contact1_name") or not request.form.get("contact1_phone") or not request.form.get("email") or not request.form.get("address") or not request.form.get("district") or not request.form.get("province"):
            error = 'Faltan datos.'
            page = 'clientes'
            return render_template("error.html", error=error, page=page)
        else:
            # Save the variables
            ruc = request.form.get("ruc")
            razon_social = request.form.get("razon_social")
            name = request.form.get("name")
            salesman = request.form.get("salesman")
            data = db.execute("SELECT id FROM users WHERE name = ?", salesman)
            sales_id = data[0]["id"]
            contact1_name = request.form.get("contact1_name")
            contact1_phone = request.form.get("contact1_phone")
            contact2_name = request.form.get("contact2_name")
            contact2_phone = request.form.get("contact2_phone")
            email = request.form.get("email")
            address = request.form.get("address")
            district = request.form.get("district")
            province = request.form.get("province")

            # Insert to the DB
            db.execute("UPDATE clients SET ruc=?, razon_social=?, name=?, salesman=?, contact1_name=?, contact1_phone=?, contact2_name=?, contact2_phone=?, email=?, address=?, district=?, province=? WHERE id=?", ruc, razon_social, name, sales_id, contact1_name, contact1_phone, contact2_name, contact2_phone, email, address, district, province, client)
            return redirect("/clientes")

    else:
        salesmen = db.execute("SELECT username, type, users.name FROM users JOIN user_type ON users.type = user_type.id AND users.type=3")
        districts = db.execute("SELECT * FROM districts")
        provinces = db.execute("SELECT * FROM provinces")
        clients = db.execute("SELECT * FROM clients WHERE id=?", client)
        salesman_client = db.execute("SELECT users.name AS salesman FROM clients JOIN users ON clients.salesman = users.id WHERE clients.id=?",client)
        print(salesman_client)
        return render_template("clients_edit.html", clients=clients, client=client, salesmen=salesmen, provinces=provinces, districts=districts, salesman_client=salesman_client)

@app.route("/productos", methods=["GET", "POST"])
@login_required
def products():

    if request.method == "POST":
        return redirect("/products-create")

    else:
        q = request.args.get("q")
        if q == "hola":
            redirect("/clients-create")
        else:
            products = db.execute("SELECT * FROM products")
            return render_template("products.html", products=products)

@app.route("/products-create", methods=["GET", "POST"])
@login_required
def products_create():

    if request.method == "POST":
        # Validate the obligatory fields are filled
        if not request.form.get("name") or not request.form.get("code") or not request.form.get("price_min") or not request.form.get("price_max"):
            error = 'Faltan datos.'
            page = 'products-create'
            return render_template("error.html", error=error, page=page)
        else:
            # Save the variables
            name = request.form.get("name")
            code = request.form.get("code")
            price_min = request.form.get("price_min")
            price_max = request.form.get("price_max")

            # Insert to the DB
            db.execute("INSERT INTO products (name, code, price_min, price_max) VALUES(?, ?, ?, ?)",
                        name, code, price_min, price_max)
            return redirect("/productos")

    else:
        return render_template("products_new.html")

@app.route('/products_edit/<product>', methods=["GET", "POST"])
@login_required
def products_edit(product):

    if request.method == "POST":
        if not request.form.get("name") or not request.form.get("code") or not request.form.get("price_min") or not request.form.get("price_max"):
            error = 'Faltan datos.'
            page = 'productos'
            return render_template("error.html", error=error, page=page)
        else:
            # Save the variables
            name = request.form.get("name")
            code = request.form.get("code")
            price_min = request.form.get("price_min")
            price_max = request.form.get("price_max")

            # Insert to the DB
            db.execute("UPDATE products SET name=?, code=?, price_min=?, price_max=? WHERE id=?", name, code, price_min, price_max, product)
            return redirect("/productos")

    else:
        products = db.execute("SELECT * FROM products WHERE id=?", product)
        return render_template("products_edit.html", products=products, product=product)

@app.route('/myaccount', methods=["GET", "POST"])
@login_required
def myaccount_edit():

    if request.method == "POST":
        # Validate the obligatory fields are filled
        if not request.form.get("name") or not request.form.get("phone") or not request.form.get("email") or not request.form.get("banco") or not request.form.get("account") or not request.form.get("birthday"):
            error = 'Faltan datos.'
            page = 'myaccount'
            return render_template("error.html", error=error, page=page)
        else:
            # Save the variables
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            bank = request.form.get("banco")
            account = request.form.get("account")
            birthday = request.form.get("birthday")

            # Update the DB
            db.execute("UPDATE clients SET salesman=? WHERE salesman=?", name, session["sales_name"])
            db.execute("UPDATE users SET name=?, phone=?, email=?, bank=?, bank_account=?, birthday=? WHERE id=?", name, phone, email, bank, account, birthday, session["user_id"])
            return redirect("/")

    else:
        banks = db.execute("SELECT * FROM banks")
        users = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        user_types = db.execute("SELECT user_type.name FROM user_type JOIN users ON user_type.id = users.type WHERE users.id=?", session["user_id"])
        return render_template("myaccount_edit.html", users=users, user_types=user_types, banks=banks)

@app.route('/editpassword', methods=["GET", "POST"])
@login_required
def password_edit():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("password_old") or not request.form.get("password_new"):
            error = 'Faltan datos.'
            page = 'editpassword'
            return render_template("error.html", error=error, page=page)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password_old")):
            error = 'Contraseña Antigua inválida.'
            page = 'editpassword'
            return render_template("error.html", error=error, page=page)

        password = request.form.get("password_new")
        hash_pass = generate_password_hash(password)

        # Redirect user to home page
        db.execute("UPDATE users SET hash=? WHERE id=?", hash_pass, session["user_id"])
        return redirect("/")

    else:
        return render_template("password_edit.html")