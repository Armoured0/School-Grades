import sqlite3
from sqlite3 import Cursor, Error

import program.database as database
import program.menu as menu
from user.admin import Admin
from user.student import Student

# functions

def saveStudentData(student, idChange=False):
    connection = database.createConnection()
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
    
    elif idChange:
        cursor.execute("""UPDATE students SET id = ? WHERE id = ?""", (student.id, student.id+1))
    
    else:
        cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
           (student.id, student.firstName, student.lastName, student.age, student.maths,
            student.english, student.physics, student.business, student.computerScience,
            student.latin))

    connection.commit()
    connection.close()

def buildStudentObject(id):
    connection = database.createConnection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    studentDbData = cursor.fetchall()
    connection.close()
    
    if studentDbData:
        studentInfo = studentDbData[0]
        return Student(studentInfo[0], studentInfo[1], studentInfo[2], 
                       studentInfo[3], studentInfo[4], studentInfo[5], 
                       studentInfo[6], studentInfo[7], studentInfo[8], 
                       studentInfo[9])
    else:
        print("Invalid student ID!")
        return False
    
def savedStudents():
    connection = database.createConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()
    connection.close()
    
    if students:
        print("--------------------")
        print("Avaliable students:")
        for student in students:
            student = buildStudentObject(student[0])
            print(f"ID: {student.id}. Full name: {student.fullName()}")
        return True
    else:
        print("No avaliable students")
        return False

def changeStudentGrade():
    enteringGrade = True
    while enteringGrade:
        usrInput = int(input("Enter grade (0-100): "))
        if usrInput >= 0 and usrInput <= 100:
            enteringGrade = False
            return usrInput
        else:
            print("Invalid percentage!")

def deleteStudentRecord(rmStudent):
    connection = database.createConnection()
    cursor = connection.cursor()
    cursor.execute("DELETE from students WHERE id = ?", (rmStudent.id,))
    connection.commit()
    cursor.execute("SELECT id from students")
    studentIds = cursor.fetchall()
    for id in studentIds:
        if id[0] > rmStudent.id:
            student = buildStudentObject(id[0])
            student.id = student.id - 1
            saveStudentData(student, True)
    connection.close()

# menu procedures

def createStudentAccount():
    choosingSave = True
    creatingStudentObject = True
    
    while creatingStudentObject:
        
        try:
            firstName = input("What is the student's first name? ")
            lastName = input("What is the student's last name? ")
            studentAge = int(input("How old is the student? "))
        
        except ValueError:
            print("Invalid input!")
        
        else:
            creatingStudentObject = False

    connection = database.createConnection()
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

def editStudentData(student):
        editing = True
        try:
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
                    print(f"Changes have been saved at {student.id}")
                    
                elif usrInput == 2:
                    print(f"Student's age is currently {student.age}")
                    student.age = input("What is the students age? ")
                    saveStudentData(student)
                    print(f"Changes have been saved at {student.id}")
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
                        
        except ValueError:
            print("Invalid option!")

def accessStudentData():
    searchingForStudent = True
    exiting = False
    accessingData = True
    while accessingData:
        while searchingForStudent:
            try:
                print("--------------------\n"
                      "How would you like to find your student?\n"
                      "1. View all available students.\n"
                      "2. Search for student by name.\n"
                      "3. Exit")
                usrInput = int(input("Choose your option: "))

                if usrInput == 1:
                    if savedStudents():
                        searchingForStudent = False
                    else:
                        searchingForStudent = False
                        accessingData = False
                        exiting = True

                elif usrInput == 2:
                    studentName = input("Enter name of student: ")
                    matches = database.studentSearch(studentName)
                    if matches:
                        print("--------------------\nMatching students accounts:")
                        for student in matches:
                            student = buildStudentObject(student[0])
                            print(f"ID: {student.id}. Full name: {student.fullName()}.")

                        searchingForStudent = False
                    else:
                        print("No matches found!")
                
                elif usrInput == 3:
                    searchingForStudent = False
                    accessingData = False
                    exiting = True
                    
                else:
                    print("Invalid option!")    

            except ValueError:
                print("Invalid option!")
                
        if not exiting:    
            print("--------------------\nEnter the ID of the student profile you would like to access.")
            id = input("Enter here: ")
            student = buildStudentObject(id)
            if student:
                usingProfile = True
                while usingProfile:
                    print(f"---- Student Profile ----\n"
                          f"ID: {student.id}\n"
                          f"Name: {student.fullName()}\n"
                          f"Age: {student.age}\n"
                          "---- Student Grades -----\n"
                          f"Maths - {student.letterGrade(student.maths)}\n"
                          f"English - {student.letterGrade(student.english)}\n"
                          f"Physics - {student.letterGrade(student.physics)}\n"
                          f"Business - {student.letterGrade(student.business)}\n"
                          f"Computer Science - {student.letterGrade(student.computerScience)}\n"
                          f"Latin - {student.letterGrade(student.latin)}\n"
                          "-------- Options --------\n"
                          "1. Edit Credentials\n"
                          "2. Add/Edit Grades\n"
                          "3. Delete Profile\n"
                          "4. Exit Menu")

                    try:
                        usrInput = int(input("Enter here: "))

                        if usrInput == 1:
                            editStudentData(student)
                        if usrInput == 2:
                            addStudentGrades(student)
                        if usrInput == 3:
                            choosing = True
                            
                            while choosing:
                                print("Are you sure you want to delete this account?")
                                usrInput = input("Enter here (Y/N): ")
                                
                                if usrInput.upper() == "Y":
                                    deleteStudentRecord(student)
                                    print("Account deleted!")
                                    
                                    choosing = False
                                    searchingForStudent = True
                                    usingProfile = False
                                elif usrInput.upper() == "N":
                                    choosing = False
                                else:
                                    print("Invalid option!")
                                
                        if usrInput == 4:
                            searchingForStudent = True
                            usingProfile = False

                    except ValueError:
                        print("Invalid option!")
            else:
                pass

def addStudentGrades(student):
    try:
        choosingGrade = True
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
                student.maths = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")

            elif usrInput == 2:
                print("Enter your english grade as a percentage.")
                student.english = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")
                
            elif usrInput == 3:
                print("Enter your physics grade as a percentage.")
                student.physics = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")
                
            elif usrInput == 4:
                print("Enter your business grade as a percentage.")
                student.business = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")
                
            elif usrInput == 5:
                print("Enter your computer science grade as a percentage.")
                student.computerScience = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")
                
            elif usrInput == 6:
                print("Enter your latin grade as a percentage.")
                student.latin = changeStudentGrade()
                saveStudentData(student)
                print(f"Changes have been saved at {student.id}")
                        
            else:
                print("Invalid option!")
        
            choosingEdit = True
            while choosingEdit:         
                print("Would you like to continue editing this student's grades?")
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
                connection = database.createConnection()
                cursor = connection.cursor()
                cursor.execute("DROP TABLE students")
                connection.close()
                database.establishTable()
                print("All student data has been reset!")
                resettingData = False
            if usrInput.upper() == "N":
                print("Exiting!")
                resettingData = False
        else:
            print("Invalid option!")
            pass
            
# main function

def main():
    database.establishTable()
    print("You must login to access this application.")
    if Admin.adminCheck() == True:
        mainRunning = True
        print("Login successful!")
        print("Welcome to the student database!")
        while mainRunning:
            print("--------------------\n"
                "Please select an option:\n"
                "1. Create new student.\n"
                "2. Access and edit student data.\n"
                "3. Reset student data.\n"
                "4. Reset admin data.\n"
                "5. Manage admin accounts.\n"
                "6. Exit program.\n"
                "--------------------")
            usrInput = input("Choose your option: ")
            if usrInput == "1":
                createStudentAccount()
            elif usrInput == "2":
                accessStudentData()
            elif usrInput == "3":
                resetStudentData()
            elif usrInput == "4":
                Admin.resetAdminData()
            elif usrInput == "5":
                Admin.manageAdminAccounts()
            elif usrInput == "6":
                menu.exitProgram()
            else:
                print("Invalid option!")
                    
            
if __name__ == '__main__':
    main()