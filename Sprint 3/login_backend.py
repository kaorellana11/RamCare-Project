import sqlite3
import bcrypt

connection_obj = sqlite3.connect('patients.db')
cursor = connection_obj.cursor()

def search_pass(username):
    cursor.execute("SELECT Password FROM Patients WHERE Username = ?", (username,))
    foundpass = cursor.fetchone()
    if foundpass is None:
        return False
    foundpass = foundpass[-1]

    return foundpass

def is_password(username, password):
    storedPass = search_pass(username)
    cursor.execute("SELECT PassSalt FROM Patients WHERE Username = ?", (username,))
    encoded = password.encode('utf-8')

    packed_salt = cursor.fetchone()
    if packed_salt is None or len(packed_salt) == 0:
        return False
    
    salt = packed_salt[-1]

    hashedPass = bcrypt.hashpw(encoded, salt)
    
    if storedPass == hashedPass:
        return True
    else:
        return False

def search_question(username, questionNum):
    if questionNum == 1:
        cursor.execute("SELECT SecQ1 FROM Patients WHERE Username = ?", (username,))
        foundquestion = cursor.fetchone()
        if foundquestion is None or len(foundquestion) == 0:
            return False
        foundquestion = foundquestion[-1]

        return foundquestion
    
    if questionNum == 2:
        cursor.execute("SELECT SecQ2 FROM Patients WHERE Username = ?", (username,))
        foundquestion = cursor.fetchone()
        if len(foundquestion) == 0:
            return False
        foundquestion = foundquestion[-1]

        return foundquestion

    if questionNum == 3:
        cursor.execute("SELECT SecQ3 FROM Patients WHERE Username = ?", (username,))
        foundquestion = cursor.fetchone()
        if len(foundquestion) == 0:
            return False
        foundquestion = foundquestion[-1]

        return foundquestion

def is_security(username, secq1, secq2, secq3):
    foundQ1 = search_question(username, 1)
    encodedQ1 = secq1.encode('utf-8')
    cursor.execute("SELECT SaltQ1 FROM Patients WHERE Username = ?", (username,))
    foundSaltQ1 = cursor.fetchone()
    if foundSaltQ1 is None or len(foundSaltQ1) == 0:
        return False
    SaltQ1 = foundSaltQ1[-1]
    hashedQ1 = bcrypt.hashpw(encodedQ1, SaltQ1)

    foundQ2 = search_question(username, 2)
    encodedQ2 = secq2.encode('utf-8')
    cursor.execute("SELECT SaltQ2 FROM Patients WHERE Username = ?", (username,))
    foundSaltQ2 = cursor.fetchone()
    if foundSaltQ1 is None or len(foundSaltQ2) == 0:
        return False
    SaltQ2 = foundSaltQ2[-1]
    hashedQ2 = bcrypt.hashpw(encodedQ2, SaltQ2)

    foundQ3 = search_question(username, 3)
    encodedQ3 = secq3.encode('utf-8')
    cursor.execute("SELECT SaltQ3 FROM Patients WHERE Username = ?", (username,))
    foundSaltQ3 = cursor.fetchone()
    if foundSaltQ3 is None or len(foundSaltQ3) == 0:
        return False
    SaltQ3 = foundSaltQ3[-1]
    hashedQ3 = bcrypt.hashpw(encodedQ3, SaltQ3)

    foundQuestions = [foundQ1, foundQ2, foundQ3]
    hashedQuestions = [hashedQ1, hashedQ2, hashedQ3]

    if foundQuestions == hashedQuestions:
        return True
    else:
        return False

def remember_me():
    cursor.execute("SELECT Username FROM Patients WHERE Remember = 1")
    foundUser = cursor.fetchone()
    if foundUser is None or len(foundUser) == 0:
        return False
    else:
        user = foundUser[-1]
        print(user)
        return user

def set_remember_false():
    if remember_me() != False:
        pastUser = remember_me()
        cursor.execute("UPDATE Patients SET Remember = 0 WHERE Username = ?", (pastUser,))
        connection_obj.commit()

def set_remember_true(username):
    set_remember_false()
    cursor.execute("UPDATE Patients SET Remember = 1 WHERE Username = ?", (username,))
    connection_obj.commit()

def main():
    username = "testuser"
    password = "testpswrd"
    q1 = "sample1"
    q2 = "sample2"
    q3 = "sample3"

    user = remember_me()
    set_remember_true(user)

    print("hi")
    #print(is_password("no one", password))
    #print(is_security("no one", "counter1", "counter2", "counter3"))

if __name__ == "__main__":
    main()