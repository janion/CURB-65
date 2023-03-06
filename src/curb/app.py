from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from datetime import datetime
from sqlite3 import connect, OperationalError
from contextlib import closing

from curb.server.calculator import calculate_curb


app = Flask(__name__)
Bootstrap(app)

with closing(connect('curb.db')) as connection:
    with closing(connection.cursor()) as cursor:
        try:
            cursor.execute("SELECT * FROM curb_score")
        except OperationalError:
            cursor.execute("CREATE TABLE curb_score(id TEXT, score INTEGER, date TEXT)")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['GET'])
def calculate():
    print("Calculate")
    return render_template('calculate.html')

@app.route('/result', methods=['POST'])
def result():
    id = request.form['id']
    dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
    confusion = bool(request.form.get('confusion', False))
    urea = int(request.form['urea'])
    resp_rate = int(request.form['resp_rate'])
    sbp = int(request.form['sbp'])
    dbp = int(request.form['dbp'])

    now = datetime.now()
    diff = now - dob
    age = int(diff.days / 365)

    curb_result = calculate_curb(confusion, urea, resp_rate, sbp, dbp, age)

    # Realised too late that I was on Python 3.5 not 3.6
    with closing(connect('curb.db')) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('INSERT INTO curb_score VALUES ("%s", "%d", "%s")' % (id, curb_result.score, now))
    return render_template('result.html', id = id, score = curb_result.score, recc = curb_result.recommendation)
