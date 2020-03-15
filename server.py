#!/usr/bin/env python2

from flask import Flask
from flask import render_template
from flask import send_file
from flask import send_from_directory
from flask import jsonify
from flask import request

from datetime import datetime

import sqlite3
import sys
import subprocess

app = Flask(__name__)

# This is the homepage, so the default page displayed
@app.route("/")
def index():
    return render_template("index.html")

# Serves the top-ten most common passwords, retrieved from the database
@app.route("/top_ten.php")
def top_ten():
    db = sqlite3.connect('/var/log/passwords.db')
    db.text_factory = str
    cursor = db.cursor()
    
    data = cursor.execute('SELECT PASSWORD,COUNT(*) from passwords group by PASSWORD order by COUNT(*) DESC LIMIT 10;')
    return jsonify({"data": [["password","count"]] + data.fetchall()})

@app.route("/latest.php")
def latest():
    db = sqlite3.connect('/var/log/passwords.db')
    db.text_factory = str
    cursor = db.cursor()
    
    data = cursor.execute('SELECT TIMESTAMP_SECS,PASSWORD from passwords group by TIMESTAMP_SECS order by TIMESTAMP_SECS DESC LIMIT 10;')
    data = data.fetchall()
    html = "Most Recent Passwords Collected:<br>"
    for timestamp,password in data:
        timestamp = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        html += "{0} : {1}<br>".format(timestamp, password)
    return html

@app.route("/stats.php")
def stats():
    db = sqlite3.connect('/var/log/passwords.db')
    db.text_factory = str
    cursor = db.cursor()
    
    data = cursor.execute('SELECT COUNT(DISTINCT PASSWORD) from passwords;')
    pwcount = data.fetchall()[0][0]
    html = "Total Unique Passwords collected: {0}<br>".format(pwcount)
    
    data = cursor.execute("SELECT COUNT(DISTINCT USERNAME) from passwords;")
    uncount = data.fetchall()[0][0]
    html += "Total Unique Usernames collected: {0}<br>".format(uncount)
    
    data = cursor.execute("SELECT COUNT(DISTINCT IP_ADDRESS) from passwords;")
    ipcount = data.fetchall()[0][0]
    html += "Total Attacking IPs seen: {0}<br>".format(ipcount)
    
    return html

@app.route("/passwords.php")
def get_passwords():
    db = sqlite3.connect('/var/log/passwords.db')
    db.text_factory = str
    cursor = db.cursor()

    data = cursor.execute('SELECT DISTINCT PASSWORD from PASSWORDS ORDER BY PASSWORD;')
    data = data.fetchall()
    
    html = '<br>\n'.join(password[0] for password in data)
    return html

@app.route("/check_password.php")
def check_password():
    word = request.args.get('check')
    word = ''.join(char for char in word if char != '"')
    pipe = subprocess.Popen(["echo", "-n", word], stdout=subprocess.PIPE)
    result = subprocess.check_output("cracklib-check", stdin=pipe.stdout)
    return result

# Runs the webserver
if __name__ == "__main__":
    run_port = int(sys.argv[-1])
    app.run(host="0.0.0.0", port=run_port)
