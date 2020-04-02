#!/usr/bin/env python2

from flask import Flask
from flask import render_template
from flask import send_file
from flask import send_from_directory
from flask import jsonify
from flask import request

from datetime import date
from datetime import datetime
from datetime import timedelta

import os
import sqlite3
import sys
import subprocess
import time

app = Flask(__name__)

latest_time = time.time()
latest_data = ""

def _fetch_latest():
    # Store time and data into cached locations
    global latest_time
    global latest_data
    now = time.time()
    # Only update the cache every 5 seconds
    if now > latest_time + 5:
        latest_time = now
        with sqlite3.connect('/var/log/passwords.db') as db:
            db.text_factory = str
            cursor = db.cursor()
            data = cursor.execute('SELECT TIMESTAMP_SECS,PASSWORD from passwords group by TIMESTAMP_SECS order by TIMESTAMP_SECS DESC LIMIT 10;')
            latest_data = data.fetchall()
    # latest_data is the cached return, which gets updated in the above block
    return latest_data

# This is the homepage, so the default page displayed
@app.route("/")
def index():
    return render_template("index.html")

# Serves the top-ten most common passwords, retrieved from the database
@app.route("/top_ten.php")
def top_ten():
    with sqlite3.connect('/var/log/passwords.db') as db:
        db.text_factory = str
        cursor = db.cursor()
        data = cursor.execute('SELECT PASSWORD,COUNT(*) from passwords group by PASSWORD order by COUNT(*) DESC LIMIT 10;')
        data = data.fetchall()
    # Format for json delivery
    words,values = zip(*data)
    
    return jsonify({"words":words, "values":values})

# This returns the newest 10 password attempts
@app.route("/latest.php")
def latest():
    data = _fetch_latest()
    offset = int(request.args.get('t'))
    html = ""
    for timestamp,password in data:
        timestamp = (datetime.utcfromtimestamp(timestamp) - timedelta(minutes=offset)).strftime("%Y-%m-%d %H:%M:%S")
        html += "{0} : {1}<br>".format(timestamp, password)
    return html

# Serves basic statistics about the current password collection operation
@app.route("/stats.php")
def stats():
    with sqlite3.connect('/var/log/passwords.db') as db:
        db.text_factory = str
        cursor = db.cursor()
        
        # Gets the count of total unique passwords
        data = cursor.execute('SELECT COUNT(DISTINCT PASSWORD) from passwords;')
        pwcount = data.fetchall()[0][0]
        html = "Total Unique Passwords collected: {0}<br>".format(pwcount)
        
        # Gets the count of total unique usernames
        data = cursor.execute("SELECT COUNT(DISTINCT USERNAME) from passwords;")
        uncount = data.fetchall()[0][0]
        html += "Total Unique Usernames collected: {0}<br>".format(uncount)
        
        # Gets the count of total attacking IPs
        data = cursor.execute("SELECT COUNT(DISTINCT IP_ADDRESS) from passwords;")
        ipcount = data.fetchall()[0][0]
        html += "Total Attacking IPs seen: {0}<br>".format(ipcount)
    
    return html

# This returns the complete list of unique passwords
@app.route("/passwords.php")
def get_passwords():
    with sqlite3.connect('/var/log/passwords.db') as db:
        db.text_factory = str
        cursor = db.cursor()

        data = cursor.execute('SELECT DISTINCT PASSWORD from PASSWORDS ORDER BY PASSWORD;')
        data = data.fetchall()
    
    html = '<br>\n'.join(password[0] for password in data)
    return html

# This checks a password against cracklib-check and returns the output
@app.route("/check_password.php")
def check_password():
    word = request.args.get('check')
    word = ''.join(char for char in word if char != '"')
    pipe = subprocess.Popen(["echo", "-n", word], stdout=subprocess.PIPE)
    result = subprocess.check_output("cracklib-check", stdin=pipe.stdout)
    return result

# This updates the password policy (using cracklib) on the server
@app.route("/update_password_policy.php")
def update_password_policy():
    with sqlite3.connect('/var/log/passwords.db') as db:
        db.text_factory = str
        cursor = db.cursor()

        data = cursor.execute('SELECT DISTINCT PASSWORD from PASSWORDS;')
        data = data.fetchall()
    
    pw_count = len(data)
    wordlist = '\n'.join(word[0] for word in data)
    with open("/com/wordlist", "w") as f:
        f.write(wordlist)
    os.system("update-cracklib")
    return "Updated {} passwords into password-blocking policy".format(pw_count)

# This gets the login attempts over the last 7 days (UTC)
@app.route("/attempts.php")
def get_attempt_counts():
    # Initialize a dictionary with the last 7 days as keys
    attempt_counter = dict()
    for d in range(7):
        current_date = (datetime.utcnow() - timedelta(days=d)).date()
        attempt_counter[current_date] = 0
    
    # Get minimum timestamp needed for database pull
    epoch = date(1970,1,1)
    min_time = int((min(attempt_counter) - epoch).total_seconds())
    
    # Pull timestamp data from database
    with sqlite3.connect('/var/log/passwords.db') as db:
        db.text_factory = str
        cursor = db.cursor()
        data = cursor.execute('SELECT TIMESTAMP_SECS from PASSWORDS WHERE TIMESTAMP_SECS > {};'.format(min_time))
        times = data.fetchall()
    
    # Count the number of attempts by date
    for time in times:
        check = datetime.utcfromtimestamp(time[0])
        if attempt_counter.get(check.date()) != None:
            attempt_counter[check.date()] += 1
    
    # Format for json delivery
    dates,values = zip(*sorted(attempt_counter.iteritems()))
    return jsonify({"dates":[str(d) for d in dates], "values":values})

# Runs the webserver
if __name__ == "__main__":
    run_port = int(sys.argv[-1])
    app.run(host="0.0.0.0", port=run_port)
