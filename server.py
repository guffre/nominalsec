#!/usr/bin/env python2

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import jsonify

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
	data = cursor.execute('SELECT password,COUNT(*) from passwords group by password order by COUNT(*) DESC LIMIT 10;')
	return jsonify({"data": [["password","count"]] + data.fetchall()})

# Runs the webserver
if __name__ == "__main__":
    run_port = int(sys.argv[-1])
    app.run(host="0.0.0.0", port=run_port)