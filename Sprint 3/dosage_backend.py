import sqlite3
import bcrypt

connection_obj = sqlite3.connect('patients.db')
cursor = connection_obj.cursor()

def create_table():
    cursor.execute("DROP TABLE IF EXISTS Patients")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            Username VARCHAR(30) NOT NULL,
            Password VARCHAR(80) NOT NULL,
            PassSalt VARCHAR(50) NOT NULL,
            SecQ1 VARCHAR(100) NOT NULL,
            SaltQ1 VARCHAR(50) NOT NULL,
            SecQ2 VARCHAR(100) NOT NULL,
            SaltQ2 VARCHAR(50) NOT NULL,
            SecQ3 VARCHAR(100) NOT NULL,
            SaltQ3 VARCHAR(50) NOT NULL,
            Dob CHAR(10) NOT NULL,
            Provider VARCHAR(100) NOT NULL,
            Medication VARCHAR(150) NOT NULL
        );
    ''')

def store_login(username, password, secq1, secq2, secq3, dob, provider, medications):
    encodedPass = password.encode('utf-8')
    passSalt = bcrypt.gensalt()
    hashedPass = bcrypt.hashpw(encodedPass, passSalt)

    encodedSecQ1 = secq1.encode('utf-8')
    saltQ1 = bcrypt.gensalt()
    hashedQ1 = bcrypt.hashpw(encodedSecQ1, saltQ1)

    encodedSecQ2 = secq2.encode('utf-8')
    saltQ2 = bcrypt.gensalt()
    hashedQ2 = bcrypt.hashpw(encodedSecQ2, saltQ2)

    encodedSecQ3 = secq3.encode('utf-8')
    saltQ3 = bcrypt.gensalt()
    hashedQ3 = bcrypt.hashpw(encodedSecQ3, saltQ3)

    cursor.execute("INSERT INTO Patients (Username, Password, PassSalt, SecQ1, SaltQ1, SecQ2, SaltQ2, SecQ3, SaltQ3, Dob, Provider, Medication) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, hashedPass, passSalt, hashedQ1, saltQ1, hashedQ2, saltQ2, hashedQ3, saltQ3, dob, provider, medications))

    connection_obj.commit()

def get_medications():
    pass

def get_provider():
    pass

