import sqlite3
from sqlite3 import Error

from classfile import Student, Admin

# other functions

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
    
    addDefaultUser = True
    for userName in adminAccounts:
        if userName[0] == "default":
            addDefaultUser = False
        else:
            pass
            
    if addDefaultUser:
        cursor.execute("INSERT INTO admins VALUES (?,?)", ('default', 'password'))
    
    connection.commit()
    connection.close()
    
def createStudentObject():
    firstName = input("What is the student's first name? ")
    lastName = input("What is the student's last name? ")
    studentAge = input("How old is the student? ")

    connection = createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM students ORDER BY id")
    allStudentIds = cursor.fetchall()
    
    connection.close()
    
    if allStudentIds:
        studentId = allStudentIds[-1][0]+1
    else:
        studentId = 0
        
    
    student = Student(studentId, firstName, lastName, studentAge)

    print(f"This student is called {student.fullName()}.\n"
          f"They are {student.age} years old.")
    
    
    return student

def saveStudentData(student):
    connection = createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM students ORDER BY id")
    studentIds = cursor.fetchall()
    
    update = False
    for id in studentIds:
        if id[0] == student.id:
            update = True
        else:
            pass    

    if update == True:
        cursor.execute("""UPDATE students SET firstName = ?, lastName = ?, age = ?, mathsGrade = ?,
                        englishGrade = ?, physicsGrade = ?, businessGrade= ?, computerScienceGrade = ?,
                        latinGrade = ? WHERE id = ?""", (student.firstName, student.lastName, student.age,
                        student.maths, student.english,student.physics, student.business, student.computerScience,
                        student.latin, student.id))
    else:
        cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
           (student.id, student.firstName, student.lastName, student.age, student.maths,
            student.english, student.physics, student.business, student.computerScience,
            student.latin))

    connection.commit()
    connection.close()

def buildStudentObject(id):
    connection = createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    studentDbData = cursor.fetchall()
    connection.close()
    
    if studentDbData:
        return Student.construct(studentDbData[0])
    else:
        print("Invalid student ID!")
        return False
       
def createAdminObject():
    creatingAdmin = True
    
    while creatingAdmin:
        userNameCheck = True
        userName = input("Select a username for your admin account: ")
        
        connection = createConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT userName FROM admins")
        adminAccounts = cursor.fetchall()
        cursor.close()
        
        for userDBName in adminAccounts:
            if userDBName[0] == userName:
                userNameCheck = False
            else:
                pass

        if userNameCheck:
            userPassword = input("Select a password for your admin account: ")

            admin = Admin(userName, userPassword)

            print(f"Your username is: {admin.userName}.\n"
                f"Your password is: {admin.password}")
            creatingAdmin = False
            return admin
        else:
            print("Username already taken. Please select another.")
                
def saveAdminData(admin):
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admins VALUES (?,?)", (admin.userName, admin.password))
    connection.commit()
    connection.close()

def buildAdminObject(userName):
    connection = createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM admins WHERE userName = ?", (userName,))
    adminDbData = cursor.fetchall()
    connection.close()
    
    if adminDbData:
        return Admin.construct(adminDbData[0])
    else:
        print("Username not found!")
        return False
    
def adminCheck():
    loggingIn = True
    while loggingIn:
        usrInput = input("Enter admin username: ")
        admin = buildAdminObject(usrInput)
        if admin:
            usrInput = input("Enter admin password: ")
            if usrInput == admin.password:
                return True
            else:
                print("Credentials incorrect!")
                return False
        else:
            pass

def savedStudents():
    connection = createConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()
    connection.close()
    
    for student in students:
        student = buildStudentObject(student[0])
        print(f"ID: {student.id}. Full name: {student.fullName()}")
    print("--------------------")

def studentCurrentGrades(student):
    return ("--------------------\n"
              "Student current grades:\n"
              f"Maths: {student.letterGrade(student.maths)}\n"
              f"English: {student.letterGrade(student.english)}\n"
              f"Physics: {student.letterGrade(student.physics)}\n"
              f"Business Studies: {student.letterGrade(student.business)}\n"
              f"Computer Science: {student.letterGrade(student.computerScience)}\n"
              f"Latin: {student.letterGrade(student.latin)}\n"
              "--------------------")

def changeStudentGrade(student):
    enteringGrade = True
    while enteringGrade:
        usrInput = int(input("Enter grade (0-100): "))
        if usrInput >= 0 and usrInput <= 100:
            enteringGrade = False
            return usrInput
        else:
            print("Invalid percentage!")

# menu procedures

def createStudent():
    choosingSave = True
    student = createStudentObject()
    while choosingSave:
        usrInput = input("Would you like to save this student? Y or N: ")
        if usrInput.upper() == "Y":
            choosingSave = False
            saveStudentData(student)
            pass
        elif usrInput.upper() == "N":
            choosingSave = False
            pass
        else:
            print("Invalid option!")
            pass

def editStudentData():
        editing = True
        try:
            print("Avaliable students:")
            savedStudents()
            print("Enter the ID of the student you would like to edit.")
            id = input("Enter here: ")
            student = buildStudentObject(id)
            while editing:
                continueEdit = True
                print("What do you want to edit?\n"
                      "1. Name\n"
                      "2. Age")
                usrInput = int(input("Enter here: "))
                if usrInput == 1:
                    print(f"Student's name is currently {student.fullName()}")
                    student.firstName = input("What is the students first name? ")
                    student.lastName = input("What is the students last name? ")
                    saveStudentData(student)
                    print(f"Changes have been saved at {id}")
                    
                elif usrInput == 2:
                    print(f"Student's age is currently {student.age}")
                    student.age = input("What is the students age? ")
                    saveStudentData(student)
                    print(f"Changes have been saved at {id}")
                else:
                    print("Invalid option!")
                    
                while continueEdit:
                    print("Would you like to continue editing?")
                    usrInput = input("Enter Here (Y/N): ")
                    if usrInput.upper() == "Y":
                        continueEdit = False
                        pass
                    elif usrInput.upper() == "N":
                        continueEdit = False
                        editing = False
                        pass
                    else:
                        print("Invalid option!")
                        pass
                        
        except FileNotFoundError:
            print("Invalid student ID!")
        except ValueError:
            print("Invalid option!")

def accessStudentData():
    selecting = True
    while selecting:
        print("Avaliable students:")
        savedStudents()
        print("Enter the ID of the data you would like to access.")
        id = input("Enter here: ")

        student = buildStudentObject(id)
        if student:
            print("Data loaded!")
            print("--------------------\n"
                  f"Student name: {student.fullName()}\n"
                  f"Student age: {student.age}")     
            print(studentCurrentGrades(student))
            
            choosingContinue = True
            while choosingContinue:         
                print("Would you like to continue accessing data?")
                usrInput = input("Enter here (Y/N): ")
                if usrInput.upper() == "Y":
                    choosingContinue = False
                elif usrInput.upper() == "N":
                    choosingContinue = False
                    selecting = False
                else:
                    print("Invalid option!")

def addStudentGrades():
    try:
        selecting = True
        while selecting:
            print("Avaliable students:")
            savedStudents()
            print("Enter the ID of the student you would like to add grades for.")
            id = input("Enter here: ")
            student = buildStudentObject(id)
            if student:
                print(studentCurrentGrades(student))
                choosingGrade = True
                selecting = False
        
        while choosingGrade:
            print("Please select a subject to edit:\n"
                  "1. Maths\n"
                  "2. English\n"
                  "3. Physics\n"
                  "4. Business\n"
                  "5. Computer Science\n"
                  "6. Latin")

            usrInput = int(input("Choose your option: "))
            
            if usrInput == 1:
                print("Enter your math grade as a percentage.")
                student.maths = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")


            elif usrInput == 2:
                print("Enter your english grade as a percentage.")
                student.english = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")
                
            elif usrInput == 3:
                print("Enter your physics grade as a percentage.")
                student.physics = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")
                
            elif usrInput == 4:
                print("Enter your business grade as a percentage.")
                student.business = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")
                
            elif usrInput == 5:
                print("Enter your computer science grade as a percentage.")
                student.computerScience = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")
                
            elif usrInput == 6:
                print("Enter your latin grade as a percentage.")
                student.latin = changeStudentGrade(student)
                saveStudentData(student)
                print(f"Changes have been saved at {id}")
                        
            else:
                print("Invalid option!")
        
            choosingEdit = True
            while choosingEdit:         
                print("Would you like to continue editing this student?")
                usrInput = input("Enter here (Y/N): ")
                if usrInput.upper() == "Y":
                    choosingEdit = False
                elif usrInput.upper() == "N":
                    choosingEdit = False
                    choosingGrade = False
                else:
                    print("Invalid option!")
                
        
    
    except ValueError:
        print("Invalid option!")
    
def resetStudentData():
    resettingData = True
    while resettingData:
        print("Are you sure you want to reset all student data?")
        usrInput = input("Enter here (Y/N): ")
        if usrInput.upper() == "Y" or usrInput.upper() == "N":
            if usrInput.upper() == "Y":
                connection = createConnection()
                cursor = connection.cursor()
                cursor.execute("DROP TABLE students")
                cursor.close()
                establishTable()
                print("All student data has been reset!")
                resettingData = False
            if usrInput.upper() == "N":
                print("Exiting!")
                resettingData = False
        else:
            print("Invalid option!")
            pass
        
def resetAdminData():
    resettingData = True
    while resettingData:
        print("Are you sure you want to reset all admin data?")
        usrInput = input("Enter here (Y/N): ")
        if usrInput.upper() == "Y" or usrInput.upper() == "N":
            if usrInput.upper() == "Y":
                connection = createConnection()
                cursor = connection.cursor()
                cursor.execute("DROP TABLE admins")
                cursor.close()
                establishTable()
                print("All admin data has been reset!")
                resettingData = False
            if usrInput.upper() == "N":
                print("Exiting!")
                resettingData = False
        else:
            print("Invalid option!")
            pass

def exitProgram():
    choosing = True
    while choosing:
        print("Are you sure you want to exit?")
        usrInput = input("Enter here (Y/N): ")
        if usrInput.upper() == "Y":
            print("Exiting...")
            exit()
        if usrInput.upper() == "N":
            choosing = False            

def createAdmin():
    choosingSave = True
    admin = createAdminObject()
    while choosingSave:
        usrInput = input("Would you like to save this account? Y or N: ")
        if usrInput.upper() == "Y":
            choosingSave = False
            saveAdminData(admin)
        elif usrInput.upper() == "N":
            choosingSave = False
        else:
            print("Invalid option!")
            pass

# main function

def main():
    establishTable()
    print("You must login to access this application.")
    if adminCheck() == True:
        mainRunning = True
        print("Login successful!")
        print("Welcome to the student database!")
        while mainRunning:
            menuRunning = True
            while menuRunning:
                try:
                    print("--------------------\n"
                        "Please select an option:\n"
                        "1. Create new student.\n"
                        "2. Edit student data.\n"
                        "3. Access student data.\n"
                        "4. Add student grades.\n"
                        "5. Reset student data.\n"
                        "6. Reset admin data. \n"
                        "7. Create admin account.\n"
                        "8. Exit.\n"
                        "--------------------")
                    usrInput = int(input("Choose your option: "))
                    if usrInput >= 1 and usrInput <= 8:
                        menuRunning = False
                        pass
                    else:
                        print("Invalid option!")
                        pass
                except ValueError:
                    print("Invalid option!")
                    pass

            if usrInput == 1:
                createStudent()
            elif usrInput == 2:
                editStudentData()
            elif usrInput == 3:
                accessStudentData()
            elif usrInput == 4:
                addStudentGrades()
            elif usrInput == 5:
                resetStudentData()
            elif usrInput == 6:
                resetAdminData()
            elif usrInput == 7:
                createAdmin()
            elif usrInput == 8:
                exitProgram()
            else:
                exit()
            
if __name__ == '__main__':
    main()