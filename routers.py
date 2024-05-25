from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)

# Функція для створення таблиці у базі даних SQLite3
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Функція для додавання нового користувача до бази даних
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashlib.sha256(password.encode()).hexdigest()))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    add_user(username, password)
    return 'Реєстрація пройшла успішно!'

if __name__ == '__main__':
    app.run(debug=True)