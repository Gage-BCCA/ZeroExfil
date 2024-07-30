from flask import Flask, render_template, request, g, redirect, jsonify
from flask_scrypt import check_password_hash, generate_password_hash, generate_random_salt
import os
import sqlite3

from csv_utils import write_link_to_csv, find_link
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

        link_object = links.create_link(link, password)
        write_link_to_csv(link_object)
        return redirect(f"/p/{link_object.new_url}")


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
@app.route("/api/secure_link", methods=['POST'])
def api_infil():
    """Takes a POST request with JSON in the body containing the original link and the password. Returns JSON with a the secured link."""
    content = request.json
    link = links.create_link(content["url"], content["password"])
    write_link_to_csv(link)
    return jsonify({"original_url": link.original_url,
                    "new_url": APP_NAME + link.new_url,
                    "id": link.new_url})

@app.route("/api/unlock_link", methods=['POST'])
def api_exfil():
    """Takes a POST request with JSON in the body containing the link ID and the password. Returns JSON with the original url for the provided link ID."""
    password = request.json["password"]
    id = request.json["id"]

    results = find_link(id)
    if not results:
        return jsonify({})
    
    hash, _, salt = results.password.partition("$")
    if check_password_hash(password, hash.encode(), salt.encode()):
        return jsonify({"url": results.original_url})
    else:
        return jsonify({})

@app.route("/api/database_info")
def api_database_info():
    """Takes a GET request and returns some information about the database."""
    pass