import sqlite3

#Patient object for easier editing
class Patient:
    def __init__(self, name, blood_type, medicines, dob, email, number):
        self.name = name
        self.blood_type = blood_type
        self.medicines = medicines
        self.dob = dob
        self.email = email
        self.number = number

    def getName(self):
        return self.name
    def setName(self, newName):
        self.name = newName

    def getBlood(self):
        return self.blood_type
    def setBlood(self, newBlood):
        self.blood_type = newBlood

    def getMedicine(self):
        return self.medicines
    def setMedicine(self, newMedicine):
        self.medicines = newMedicine

    def getDob(self):
        return self.dob
    def setDob(self, newDate):
        self.dob = newDate

    def getEmail(self):
        return self.email
    def setEmail(self, newEmail):
        self.email = newEmail

    def getNumber(self):
        return self.number
    def setNumber(self, newNumber):
        self.number = newNumber

#In order to execute SQL commands to edit the database, we need to first connect
#to the SQLite database. If a database file does not exist, one will automatically
#be created.
connection_obj = sqlite3.connect('ramcare.db')

#Then, we create a cursor object. The cursor object will act as a middleman between
#the SQLite database and SQL commands.
cursor = connection_obj.cursor() 

def create_table():
    #Clear the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS RAMCARE")

    #SQL works weird. You must make a query as a variable and then execute that query.
    #You don't necessarily have to make it a variable, but I'll be doing so for now.
    cursor.execute('''
        CREATE TABLE RAMCARE (
            Name VARCHAR(30) NOT NULL,
            Blood_Type CHAR(5) NOT NULL,
            Medicines VARCHAR(50) NOT NULL,
            Date_of_birth CHAR(10) NOT NULL,
            Email VARCHAR(30) NOT NULL,
            Phone_Number CHAR(14) NOT NULL
        );
    ''')

def insert_data(name, blood_type, medicines, dob, email, number):
    #Insert Data
    cursor.execute("INSERT INTO RAMCARE (Name, Blood_Type, Medicines, Date_of_birth, Email, Phone_Number) VALUES (?, ?, ?, ?, ?, ?)", (name, blood_type, medicines, dob, email, number))

    #Make sure to commit the changes to the database
    connection_obj.commit()

def create_patient(name, blood_type, medicines, dob, email, number):
    insert_data(name, blood_type, medicines, dob, email, number)
    print("Patient Successfully Entered")

def search_by_name(name):
    cursor.execute("SELECT * from RAMCARE WHERE Name = ?", (name,))
    print(cursor.fetchall())
    connection_obj.commit()
    print("Data successfully retrieved")

def main():
    create_table()

    name = "Robert Smith"
    blood_type = "AB+"
    medicines = "Tylenol"
    dob = "03/21/2005"
    email = "smithre9@vcu.edu"
    number = "(702)-539-5013"

    insert_data(name, blood_type, medicines, dob, email, number)
    print("Data successfully inserted")
    insert_data("Kay Orellana", "O-", "Ibuprofen", "10/04/2004", "kaorellana52@gmail.com", "(123)-456-7890")


    search_by_name("Kay Orellana")


if __name__ == '__main__':
    main()

#Close the connection to the database
connection_obj.close()