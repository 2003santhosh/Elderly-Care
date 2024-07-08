from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3
import hashlib
import os,json
import subprocess

app = Flask(__name__)
app.secret_key = 'secret_key'

db_file = 'users.db'
if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(name, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        conn.close()
        return True 
    except sqlite3.IntegrityError:
        conn.close()
        return False 

def validate_login(email, password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, hashlib.sha256(password.encode()).hexdigest()))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route('/login', methods=['POST'])
def login():
    email = request.form['name'] 
    password = request.form['password']


    user = validate_login(email, password)

    if user:
    
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        return jsonify({"success": True})
    else:
    
        return jsonify({"success": False, "message": "Invalid email or password"})


def run_django_app(port):
    django_app_path = 'manage.py'
    subprocess.Popen(['python', django_app_path, 'runserver', f'127.0.0.1:{port}'])

@app.route('/logged_page')
def logged_page():
    
    django_port = 8001 

    run_django_app(django_port)

    return redirect(f'http://127.0.0.1:{django_port}')


@app.route('/')
def login_pg():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    if register_user(name, email, password):
        return "Registration successful"
    else:
        return "Registration failed. Email already in use"

@app.route('/register_pg')
def register_page():
    return render_template('register.html')

@app.route('/home_page')
def home_page():
    return render_template('home.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
