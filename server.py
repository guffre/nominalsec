#!/usr/bin/env python2

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import jsonify

from datetime import datetime

import sqlite3
import sys

app = Flask(__name__)

# This is the homepage, so the default page displayed
@app.route("/")
def index():
    return render_template("index.html")

# This serves javascript files from the static/js directory
@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

# Serves the top-ten most common passwords, retrieved from the database
@app.route("/top_ten.php")
def top_ten():
	db = sqlite3.connect('/var/log/passwords.db')
	cursor = db.cursor()
	data = cursor.execute('SELECT PASSWORD,COUNT(*) from passwords group by PASSWORD order by COUNT(*) DESC LIMIT 10;')
	return jsonify({"data": [["password","count"]] + data.fetchall()})

@app.route("/latest.php")
def latest():
    db = sqlite3.connect('/var/log/passwords.db')
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
    cursor = db.cursor()
    
    data = cursor.execute('SELECT COUNT(DISTINCT PASSWORD) from passwords;')
    pwcount = data.fetchall()
    html = "Total Unique Passwords collected: {0}<br>".format(pwcount)
    
    data = cursor.execute("SELECT COUNT(DISTINCT USERNAME) from passwords;")
    uncount = data.fetchall()
    html += "Total Unique Usernames collected: {0}<br>".format(uncount)
    
    data = cursor.execute("SELECT COUNT(DISTINCT IP_ADDRESS) from passwords;")
    ipcount = data.fetchall()
    html += "Total Attacking IPs seen: {0}<br>".format(ipcount)
    
    return html

# Runs the webserver
if __name__ == "__main__":
    run_port = int(sys.argv[-1])
    app.run(host="0.0.0.0", port=run_port)

