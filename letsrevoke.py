import os
import sqlite3

from contextlib import closing
from flask import Flask, request, render_template


LETSWIFI_DB = 'letswifi-dev.sqlite'


def db_read_ca(filename='letswifi-dev.sqlite'):
    ca = {}
    with closing(sqlite3.connect(filename)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM ca").fetchall()

    for row in rows:
        ca[row[0]] = {
            'pub': row[1],
            'key': row[2],
            'issuer': row[3]
        }
    return ca


def db_read_issued(filename=LETSWIFI_DB):
    with closing(sqlite3.connect(filename)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM realm_signing_log").fetchall()
    return rows


def crl_create():
    pass


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(128)

    @app.route('/', methods=['POST', 'GET'])
    def index():
        issued = db_read_issued()
        ca = db_read_ca()

        if request.method == 'POST':
            selected = request.form
            for item in selected:
                serial = item[0]

                for row in issued:
                    if int(serial) != row[0]:
                        continue
                    pub = ca[row[2]]['pub']
                    key = ca[row[2]]['key']
                    serial = row[0]

                    # We should make a CRL from this
                    print(f'{pub} {key} {serial}')

        return render_template("index.html", issued=issued)

    app.run(debug=True, host='0.0.0.0', port=8080)
