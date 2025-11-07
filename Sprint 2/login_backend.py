import sqlite3
import hashlib

connection_obj = sqlite3.connect('login.db')
cursor = connection_obj.cursor

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Login (
            Username VARCHAR(30) NOT NULL
            Password VARCHAR(50) NOT NULL
        );
    ''')

def store_login(username, password):
    cursor.execute("INSERT INTO Login (Username, Password) VALUES (?, ?)", (username, password))
    #sort_user() // Don't know if needed yet

    connection_obj.commit()

def sort_user():
    cursor.execute('''
        CREATE TABLE Login_ordered (
            Username VARCHAR(30) NOT NULL,
            Password VARCHAR(50) NOT NULL
        );
    ''')
    cursor.execute("INSERT INTO Login_ordered (Username, Password) SELECT Username, Password FROM Login ORDER BY Username;")

def search_pass(username):
    password = cursor.execute("SELECT Password FROM Login WHERE Username = ?", (username))
    return password

def is_password(username, password):
    login_pass = search_pass(username)
    if login_pass == password:
        return True
    else:
        return False

