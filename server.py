#!/usr/bin/env python2

from flask import Flask
from flask import render_template
from flask import jsonify

import sqlite3
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.js")
def index_scripts():
    return render_template("static/js/index.js")

@app.route("/top_ten.php")
def top_ten():
	db = sqlite3.connect('/var/log/passwords.db')
	cursor = db.cursor()
	data = cursor.execute('SELECT password,COUNT(*) from passwords group by password order by COUNT(*) DESC LIMIT 10;')
	data = {k:v for k,v in data.fetchall()}
	data = sorted(data.iteritems(), reverse=True, key=lambda x: x[1])
	return jsonify(data)

if __name__ == "__main__":
    run_port = int(sys.argv[-1])
    app.run(host="0.0.0.0", port=run_port)

