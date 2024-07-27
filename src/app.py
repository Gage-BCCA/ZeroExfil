from flask import Flask, render_template, request, g, redirect
from flask_scrypt import check_password_hash, generate_password_hash, generate_random_salt
import os
import sqlite3

from csv_utils import write_link_to_csv, find_link, verify_id_uniqueness
import links

app = Flask(__name__)

APP_NAME = '127.0.0.1:5000/0/'
PROTOCOL = 'http://'


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/0/<id>")
def url_gate(id: str):
    results = find_link(id)
    if not results:
        return redirect('/')
    return render_template('url_gate.html', id=id)


@app.route('/secure', methods=["POST"])
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

        # Input Validation
        if not link:
            return "<p>Bad</p>"
        if not password:
            return "<p>Bad</p>"

        # Password Salting and Hashing
        salt = generate_random_salt()
        pwd_hash = generate_password_hash(password, salt)
        pwd_and_hash = pwd_hash + b"$" + salt
        #print(pwd_and_hash.decode('utf-8'))

        # New URL Generation
        new_path = links.generate_random_string()
        while not verify_id_uniqueness(new_path):
            new_path = links.generate_random_string()

        link_object = links.Link(original_url=link, 
                                 new_url=new_path, 
                                 password=pwd_and_hash.decode(), # We have to decode this here to make sure the "b" does not get added to the byte string
                                 )
        
        write_link_to_csv(link_object)

        return redirect(f"/p/{new_path}")


@app.route("/unlock", methods=['POST'])
def decode():
    if request.method == "POST":
        password = request.form["password"]
        id = request.form["id"]

        results = find_link(id)
        if not results:
            return redirect('/')
        
        hash, _, salt = results.password.partition("$")
        if check_password_hash(password, hash.encode(), salt.encode()):
            return redirect(results.original_url)
        else:
            return redirect(f"/0/{id}")
        
        
@app.route("/p/<id>")
def protected_url(id):
    url = PROTOCOL + APP_NAME + id
    return render_template("protected_url.html", url=url)


#############################
#          REST API         #
#############################
@app.route("/api/secure_link")
def api_infil():
    pass

@app.route("/api/unlock_link")
def api_exfil():
    pass

@app.route("/api/database_info")
def api_database_info():
    pass