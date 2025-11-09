import sqlite3
import bcrypt

connection_obj = sqlite3.connect('login.db')
cursor = connection_obj.cursor()

def create_table():
    cursor.execute("DROP TABLE IF EXISTS Login")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Login (
            Username VARCHAR(30) NOT NULL,
            Password VARCHAR(80) NOT NULL,
            Salt VARCHAR(50) NOT NULL,
            SecQ1 VARCHAR(100) NOT NULL,
            SecQ2 VARCHAR(100) NOT NULL,
            SecQ3 VARCHAR(100) NOT NULL
        );
    ''')

def store_login(username, password, secq1, secq2, secq3):
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPass = bcrypt.hashpw(encoded, salt)
    cursor.execute("INSERT INTO Login (Username, Password, Salt, SecQ1, SecQ2, SecQ3) VALUES (?, ?, ?, ?, ?, ?)", (username, hashedPass, salt, secq1, secq2, secq3))
    #sort_user() // Don't know if needed yet

    connection_obj.commit()

def sort_user():
    cursor.execute('''
        CREATE TABLE Login_ordered (
            Username VARCHAR(30) NOT NULL,
            Password VARCHAR(50) NOT NULL
            Salt VARCHAR(50) NOT NULL,
            SecQ1 VARCHAR(100) NOT NULL,
            SecQ2 VARCHAR(100) NOT NULL,
            SecQ3 VARCHAR(100) NOT NULL
        );
    ''')
    cursor.execute("INSERT INTO Login_ordered (Username, Password, Salt, SecQ1, SecQ2, SecQ3) SELECT Username, Password, Salt, SecQ1, SecQ2, SecQ3 FROM Login ORDER BY Username;")

def search_pass(username):
    cursor.execute("SELECT Password FROM Login WHERE Username = ?", (username,))
    foundpass = cursor.fetchone()
    foundpass = foundpass[-1]

    return foundpass

def is_password(username, password):
    storedPass = search_pass(username)
    cursor.execute("SELECT Salt FROM Login WHERE Username = ?", (username,))
    encoded = password.encode('utf-8')

    packed_salt = cursor.fetchone()
    if len(packed_salt) == 0:
        return False
    
    salt = packed_salt[-1]

    hashedPass = bcrypt.hashpw(encoded, salt)
    
    if storedPass == hashedPass:
        return True
    else:
        return False

def main():
    create_table()

    username = "smithre9"
    password = "burgerman"

    store_login(username, password)

    print(is_password(username, password))

if __name__ == "__main__":
    main()