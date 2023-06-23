from flask import Flask, render_template, request, g, redirect
import sqlite3
import threading

app = Flask(__name__)

DATABASE = 'data.db'

# Create a connection to the SQLite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create a table to store the input data
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS input_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT,
            sentiment TEXT
        )
    ''')
    conn.commit()

# Initialize the database connection before each request
@app.before_request
def before_request():
    g.db = get_db()
    create_table()

# Close the database connection after each request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    sentence = request.form['sentence']
    sentiment = request.form['sentiment']

    # Insert the input data into the database
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO input_data (sentence, sentiment) VALUES (?, ?)', (sentence, sentiment))
    g.db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
