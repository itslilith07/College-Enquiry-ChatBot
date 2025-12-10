from chatbot import chatbot
from flask import Flask, render_template, request, session, url_for, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.static_folder = 'static'

def get_db():
    db = sqlite3.connect('users.db')
    db.row_factory = sqlite3.Row
    return db

# Create tables if they don't exist
with get_db() as db:
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS suggestion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    db.commit()

# Google recaptcha - site key : 6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L
# Google recaptcha - secret key : 6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                     (email, password)).fetchone()
    
    if user:
        session['id'] = user['id']
        flash('You were successfully logged in')
        return redirect('/index')
    else:
        flash('Invalid credentials !!!')
        return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    
    db = get_db()
    try:
        db.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                  (name, email, password))
        db.commit()
        
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        flash('You have successfully registered!')
        session['id'] = user['id']
        return redirect('/index')
    except sqlite3.IntegrityError:
        flash('Email already exists!')
        return redirect('/register')

@app.route('/suggestion', methods=['POST'])
def suggestion():
    email = request.form.get('uemail')
    suggesMess = request.form.get('message')
    
    db = get_db()
    db.execute('INSERT INTO suggestion (email, message) VALUES (?, ?)',
               (email, suggesMess))
    db.commit()
    
    flash('Your suggestion was successfully sent!')
    return redirect('/index')


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    # app.secret_key=""
    app.run() 
