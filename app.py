from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime as dt
import sqlite3

app = Flask(__name__)

# Function to create the database and tables if they don't exist
def initialize_database():
    connection = sqlite3.connect("loginData.db")
    cursor = connection.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    connection.commit()
    connection.close()

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # Create notes table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
        noteTitle TEXT PRIMARY KEY,
        noteDesc TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )''')

    connection.commit()
    connection.close()

# Call function to initialize the database
initialize_database()

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect('loginData.db', check_same_thread=False)
        cursor = connection.cursor()

        # Check if the email is already registered
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('login.html', error='Email already registered.')

        # Insert new user
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))

        connection.commit()
        connection.close()

        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect('loginData.db')
        cursor = connection.cursor()

        # Verify user credentials
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            print("Login Success")
            return redirect(url_for('index'))
        else:
            print("Login error")
            return render_template('login.html', error='Invalid email or password.')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def submit():
    connect = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connect.cursor()

    title = request.form['title']
    desc = request.form['desc']

    dateCreated = dt.today().date()
    hourCreated = f"{dt.now().hour:02d}"
    minCreated = f"{dt.now().minute:02d}"

    record = [(title, desc, str(dateCreated), f"{hourCreated}:{minCreated}")]

    try:
        cursor.executemany("INSERT INTO notes VALUES (?, ?, ?, ?)", record)
        connect.commit()
        return render_template('success.html')
    except sqlite3.IntegrityError:
        connect.rollback()
        error_message = 'Note with the same title already exists.'
        return render_template('create.html', error=error_message)
    finally:
        connect.close()

@app.route('/display')
def displayNotes():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT noteTitle, noteDesc, date, time FROM notes")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('display.html', rows=rows)

@app.route('/note/<int:note_id>')
def display_note(note_id):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes WHERE rowid = ?", (note_id,))
    note = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('note.html', note=note, note_id=note_id)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        cursor.execute("UPDATE notes SET noteTitle = ?, noteDesc = ? WHERE rowid = ?", (title, desc, note_id))
        connection.commit()

        cursor.execute("SELECT * FROM notes WHERE rowid = ?", (note_id,))
        note = cursor.fetchone()
        return render_template('note.html', note=note, note_id=note_id)
    else:
        cursor.execute("SELECT * FROM notes WHERE rowid = ?", (note_id,))
        note = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return render_template('edit.html', note=note, note_id=note_id)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # Delete the note
    cursor.execute("DELETE FROM notes WHERE rowid = ?", (note_id,))

    connection.commit()
    connection.close()

    return redirect(url_for('displayNotes'))

if __name__ == '__main__':
    app.run(debug=True)
