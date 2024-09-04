import datetime

import sqlite3
from flask import Flask, request, jsonify, render_template, g

from bible import get_book_name_by_id

app = Flask(__name__)

DATABASE = 'bible.db'

def get_db():
    # Open a new database connection if there is none yet for the current application context
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    # Close the database again at the end of the request
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [
        datetime.datetime(2018, 1, 1, 10, 0, 0),
        datetime.datetime(2018, 1, 2, 10, 30, 0),
        datetime.datetime(2018, 1, 3, 11, 0, 0),
    ]

    return render_template("index.html", times=dummy_times)

@app.route("/search", methods=['GET'])

def search_keywords():
    keyword = request.args.get('keyword', '')
    bookId = request.args.get('bookId', '')
    testment = request.args.get('testament', '')

    if not keyword:
        return jsonify("No keyword provided")
    
    basequery = 'SELECT * FROM verses WHERE LOWER(content) LIKE ?'
    params = ['%' + keyword.lower() + '%']

    if bookId:
        basequery += ' AND book = ?'
        params.append(bookId)

    if testment == 'OT':
        basequery += ' AND book between 1 AND 39'
    elif testment == 'NT':
        basequery += ' AND book between 40 AND 66'

    db = get_db()
    cursor = db.cursor()
    cursor.execute(basequery, params)

    results = cursor.fetchall()
    # Convert results into a list of dictionaries
    results = [{'id': row[0], 'book': get_book_name_by_id(row[1]), 'chapter': row[2], 'verse': row[3], 'content': row[4]} for row in results]
    return jsonify(results)

@app.route('/api', methods=['GET'])
def api():
    return jsonify("API is working")

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)