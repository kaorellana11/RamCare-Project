import sqlite3
import bcrypt
import login_backend

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
            Remember INTEGER NOT NULL,
            Dob CHAR(10) NOT NULL,
            Provider VARCHAR(100) NOT NULL,
            Medication VARCHAR(100) NOT NULL,
            Dosage INTEGER NOT NULL
        );
    ''')

def store_login(username, password, secq1, secq2, secq3, remember, dob, provider, medications, dosage):
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

    cursor.execute("INSERT INTO Patients (Username, Password, PassSalt, SecQ1, SaltQ1, SecQ2, SaltQ2, SecQ3, SaltQ3, Remember, Dob, Provider, Medication, Dosage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, hashedPass, passSalt, hashedQ1, saltQ1, hashedQ2, saltQ2, hashedQ3, saltQ3, remember, dob, provider, medications, dosage))

    connection_obj.commit()

def get_dob(username):
    cursor.execute("SELECT Dob FROM Patients WHERE Username = ?", (username,))
    foundDob = cursor.fetchone()
    if foundDob is None:
        return False
    foundDob = foundDob[-1]

    return foundDob

def get_medications(username):
    cursor.execute("SELECT Medication FROM Patients WHERE Username = ?", (username,))
    foundMeds = cursor.fetchone()
    if foundMeds is None:
        return False
    foundMeds = foundMeds[-1]

    character = ','
    if character in foundMeds:
        foundMeds = foundMeds.split(',')

    return foundMeds

def get_provider(username):
    cursor.execute("SELECT Provider FROM Patients WHERE Username = ?", (username,))
    foundProv = cursor.fetchone()
    if foundProv is None:
        return False
    foundProv = foundProv[-1]

    return foundProv

def confirm_dosage(username):
    cursor.execute("UPDATE Patients SET Dosage = True WHERE Username = ?", (username,))
    connection_obj.commit()
    print("Patient Dosage Taken Confirmed")

def next_day():
    cursor.execute("UPDATE Patients SET Dosage = False")
    connection_obj.commit()
    print("Patients Confirmation Reset")

def main():
    create_table()

    username = "testuser"
    password = "testpswrd"
    q1 = "sample1"
    q2 = "sample2"
    q3 = "sample3"
    remember = False
    dob = "01/01/1999"
    provider = "Dominion Medical Associates"
    medications = "Tylenol"
    dosage = False

    store_login(username, password, q1, q2, q3, remember, dob, provider, medications, dosage)

    testProv = get_provider(username)
    if (testProv == provider):
        print("Get Provider works")
    
    testMeds = get_medications(username)
    if (testMeds == medications):
        print("Get Medications works")
    
    confirm_dosage(username)
    next_day()
    
if __name__ == "__main__":
    main()

