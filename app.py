from flask import Flask, render_template, request, g, redirect, jsonify
import sqlite3
import threading
import pickle


app = Flask(__name__)



filename = 'model.pkl'
loaded_model, loaded_vectorizer = pickle.load(open(filename, 'rb'))

# Function to process the sentence
def process_sentence(sentence):
    new_sentence_vectorized = loaded_vectorizer.transform([sentence])
    predicted_sentiment = loaded_model.predict(new_sentence_vectorized)
    if predicted_sentiment[0] == -1:
        return "negative"
    else:
        return "positive"
        

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

@app.route('/text/<text>', methods=['GET'])
def get_user(text):
    # Perform logic to retrieve user data based on the username
    user_data = {
        'text': text,
        'sent': process_sentence(text)
    }
    response = jsonify(user_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/entry')
def entry():
    return render_template('entry.html')

@app.route('/submit', methods=['POST'])
def submit():
    sentence = request.form['sentence']
    sentiment = request.form['sentiment']

    # Insert the input data into the database
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO input_data (sentence, sentiment) VALUES (?, ?)', (sentence, sentiment))
    g.db.commit()

    return redirect('/entry')

if __name__ == '__main__':
    app.run()