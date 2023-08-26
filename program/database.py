import sqlite3
from sqlite3 import Cursor, Error

def createConnection(dbFile="SchoolDatabase.sqlite"):
    connection = None
    try:
        return sqlite3.connect(dbFile)
    except Error as error:
        print(error)
        exit()
    finally:
        if connection:
            connection.close()
            
def establishTable():
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS students (
                       id INTEGER,
                       firstName TEXT,
                       lastName TEXT,
                       age INTEGER,
                       mathsGrade INTEGER,
                       englishGrade INTEGER,
                       physicsGrade INTEGER,
                       businessGrade INTEGER,
                       computerScienceGrade INTEGER,
                       latinGrade INTEGER
                   )""")
    
    cursor.execute("""
               CREATE TABLE IF NOT EXISTS admins (
                   userName TEXT,
                   password TEXT
               )""")
    
    cursor.execute("SELECT userName FROM admins")
    adminAccounts = cursor.fetchall()
    
    addDefaultAdminUser = True
    for user in adminAccounts:
        if user[0] == "default":
            addDefaultAdminUser = False
    
    
    if addDefaultAdminUser:
        cursor.execute("INSERT INTO admins VALUES (?,?)", ('default', 'password'))
    
    connection.commit()
    connection.close()
    
    
def studentSearch(query):
    results = []
    connection = createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, firstName, lastName FROM students")
    students = cursor.fetchall()
    
    for student in students:
        if query.lower() in f"{student[1].lower()} {student[2].lower()}":
            results.append(student)
                     
    connection.close()
    return results

if __name__ == '__main__':
    print("Please run the main script!")