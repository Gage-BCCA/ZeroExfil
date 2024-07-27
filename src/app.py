from flask import Flask, render_template, request, g, redirect
from flask_scrypt import check_password_hash, generate_password_hash, generate_random_salt, debase64
import os
import sqlite3

import links

app = Flask(__name__)

DATABASE = 'links.db'
APP_NAME = '127.0.0.1:5000/0/'
PROTOCOL = 'http://'


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/0/<id>")
def url_gate(id: str):
    results = query_db("SELECT new_url, retries FROM links WHERE new_url=?", [id,], one=True)
    if not results:
        return f"<h1>No Results</h1>"
    
    return render_template('url_gate.html', id=id)


@app.route('/infil', methods=["POST"])
def secure():
    """
    Bread and butter for the app. Takes a POST request from a form on the homepage that includes
    the password, link, and number of retries (which is optional). Afterwards, it safely stores the password by 
    salting it and hashing it. A new URL is generated, and then this information is appended to the database.
    """
    if request.method == "POST":

        # Information Gathering
        link = request.form["link"]
        password = request.form["password"]
        retries = request.form["retries"]

        # Input Validation
        if not link:
            return "<p>Bad</p>"
        if not password:
            return "<p>Bad</p>"
        if not retries or int(retries) == 0:
            retries = 0

        # Password Salting and Hashing
        salt = generate_random_salt()
        pwd_hash = generate_password_hash(password, salt)
        pwd_and_hash = pwd_hash + b"$" + salt
        #print(pwd_and_hash.decode('utf-8'))

        # New URL Generation
        new_path = links.generate_random_string()
        while not verify_string_uniqueness(new_path):
            new_path = links.generate_random_string()

        link_object = links.Link(original_url=link, 
                                 new_url=new_path, 
                                 password=pwd_and_hash, 
                                 retries=retries,
                                 attempts=0)
        
        get_db().execute("INSERT INTO links (original_url, new_url, password, retries, attempts) VALUES (?, ?, ?, ?, ?)", 
                         link_object.get_link_data())
        
        get_db().commit()
        get_db().close()

        return redirect(f"/p/{new_path}")


def verify_string_uniqueness(new_url: str) -> bool:
    results = query_db("SELECT * FROM links WHERE new_url = ?", [new_url,])
    if not results:
        return True
    return False


@app.route("/exfil", methods=['POST'])
def decode():
    if request.method == "POST":
        password = request.form["password"]
        id = request.form["id"]

        results = query_db("SELECT * FROM links WHERE new_url=?", [id,], one=True)
        hash, _, salt = results["password"].decode().partition("$")

        if check_password_hash(password, hash.encode(), salt):
            return redirect(results["original_url"])
        else:
            return redirect(f"/0/{id}")
        
        
@app.route("/p/<id>")
def protected_url(id):
    url = PROTOCOL + APP_NAME + id
    return render_template("protected_url.html", url=url)


######################################
#         Database Functions         #
######################################

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv