import pickle
import os


from classfile import Student, Admin


def createStudentObject():
    firstName = input("What is the student's first name? ")
    lastName = input("What is the student's last name? ")
    studentAge = input("How old is the student? ")

    student = Student(firstName, lastName, studentAge, None, None)

    print(f"This student is called {student.fullName()}.\n"
          f"They are {student.age} years old.")
    return student

def saveStudentData(student):
    try:
        with open('StudentIdCount.txt', 'r') as idCount:
            id = idCount.read()
        with open(f'Student_Data\\{id}', 'wb') as f:
            pickle.dump(student, f)

        with open(f'Student_Data\\{id}', 'rb') as r:
            student = pickle.load(r)
            print(f"{student.fullName()} has been saved at {id}")

        with open('StudentIdCount.txt', 'w') as idCount:
            id = int(id) + 1
            idCount.write(str(id))
    except:
        print("Save failed.")
        pass

def createAdminObject():
    creatingAdmin = True
    
    while creatingAdmin:
        userNameCheck = True
        userName = input("Select a username for your admin account: ")
        for file in os.listdir('Admin_Data'):
            if file == userName:
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
    try:
        with open(f'Admin_Data\\{admin.userName}', 'wb') as f:
            pickle.dump(admin, f)

        with open(f'Admin_Data\\{admin.userName}', 'rb') as r:
            admin = pickle.load(r)
            print(f"{admin.userName} has been saved.")   
    except:
        print("Save failed.")
        pass

def adminCheck():
    loggingIn = True
    while loggingIn:
        usrInput = input("Enter admin username: ")
        for file in os.listdir('Admin_Data'):
            if file == usrInput:
                with open(f'Admin_Data\\{file}', 'rb') as r:
                    admin = pickle.load(r)
                    usrInput = input("Enter admin password: ")
                    if usrInput == admin.password:
                        return True
                    else:
                        print("Credentials incorrect!")
                        return False
        print("Username not found!")



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
            for file in os.listdir('Student_Data'):
                if file != ".gitkeep":
                    with open(f'Student_Data\\{file}', 'rb') as r:
                        student = pickle.load(r)
                        print(f"ID:{file}. Full name: {student.fullName()}")
            print("Enter the ID of the student you would like to edit.")
            id = input("Enter here:")
            with open(f'Student_Data\\{id}', 'rb') as r:
                student = pickle.load(r)
            while editing:
                continueEdit = True
                print("What do you want to edit?\n"
                      "1. Name\n"
                      "2. Age")
                usrInput = int(input("Enter here:"))
                if usrInput == 1:
                    print(f"Student's name is currently {student.fullName()}")
                    student.firstName = input("What is the students first name?")
                    student.lastName = input("What is the students last name?")
                    with open(f'Student_Data\\{id}', 'wb') as f:
                        pickle.dump(student, f)
                        print(f"Changes have been saved at {id}")
                    
                elif usrInput == 2:
                    print(f"Student's age is currently {student.age}")
                    student.age = input("What is the students age?")
                    with open(f'Student_Data\\{id}', 'wb') as f:
                        pickle.dump(student, f)
                        print(f"Changes have been saved at {id}")
                else:
                    print("Invalid option!")
                    
                while continueEdit:
                    print("Would you like to continue editing?")
                    usrInput = input("Enter Here (Y/N): ")
                    if usrInput == "Y":
                        continueEdit = False
                        pass
                    elif usrInput == "N":
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
    print("Avaliable students:")
    for file in os.listdir('Student_Data'):
        with open(f'Student_Data\\{file}', 'rb') as r:
            if file != ".gitkeep":
                student = pickle.load(r)
                print(f"ID: {file}. Full name: {student.fullName()}")
    print("Enter the ID of the data you would like to access.")
    id = input("Enter here:")
    try:
        with open(f'Student_Data\\{id}', 'rb') as r:
            student = pickle.load(r)
            print("Data loaded!")
            print(f"Student full name: {student.fullName()}\n"
                  f"Student age: {student.age}\n"
                  f"Maths grade: {student.letterGrade(student.maths)}\n"
                  f"English grade: {student.letterGrade(student.english)}")
    except FileNotFoundError:
        print("Invalid student ID!")

def addStudentGrades():
    try:
        
        print("Avaliable students:")
        for file in os.listdir('Student_Data'):
            with open(f'Student_Data\\{file}', 'rb') as r:
                if file != ".gitkeep":
                    student = pickle.load(r)
                    print(f"ID:{file}. Full name: {student.fullName()}")
        print("Enter the ID of the student you would like to add grades for.")
        id = input("Enter here:  ")
        with open(f'Student_Data\\{id}', 'rb') as r:
            student = pickle.load(r)
            
        print("Student current grades:\n"
              f"Maths: {student.letterGrade(student.maths)}\n"
              f"English: {student.letterGrade(student.english)}")

        choosingGrade = True
        
        while choosingGrade:
            print("Please select a subject to edit:\n"
                  "1. Maths\n"
                  "2. English")

            usrInput = int(input("Choose your option: "))
            if usrInput == 1:
                enteringGrade = True
                print("Enter your math grade as a percentage.")
                while enteringGrade:
                    usrInput = int(input("Enter grade (0-100): "))
                    if usrInput > 0 and usrInput <= 100:
                        student.maths = usrInput
                        with open(f'Student_Data\\{id}', 'wb') as f:
                            pickle.dump(student, f)
                        print(f"Changes have been saved at {id}")
                        enteringGrade = False
                    else:
                        print("Invalid percentage!")

            if usrInput == 2:
                enteringGrade = True
                print("Enter your english grade as a percentage.")
                while enteringGrade:
                    usrInput = int(input("Enter grade (0-100): "))
                    if usrInput > 0 and usrInput <= 100:
                        student.english = usrInput
                        with open(f'Student_Data\\{id}', 'wb') as f:
                            pickle.dump(student, f)
                        print(f"Changes have been saved at {id}")
                        enteringGrade = False
                    else:
                        print("Invalid percentage!")
        
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
    except FileNotFoundError:
        print("Student ID not found!")
    
def resetStudentData():
    resettingData = True
    while resettingData:
        print("Are you sure you want to reset all student data?")
        usrInput = input("Enter here (Y/N): ")
        if usrInput.upper() == "Y" or usrInput.upper() == "N":
            if usrInput.upper() == "Y":
                with open('StudentIdCount.txt', 'w') as idCount:
                     idCount.write("0")
                for file in os.listdir('Student_Data'):
                    if file != ".gitkeep":
                        os.remove(f"Student_Data\\{file}")
                        print("All student has been reset!")
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
                for file in os.listdir('Admin_Data'):
                    if file != ".gitkeep" and file != "default":
                        os.remove(f"Admin_Data\\{file}")
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


def main():
    print("You must login to access this application.")
    if adminCheck() == True:
        mainRunning = True
        print("Login successful!")
        print("Welcome to the student database!")
        while mainRunning:
            startUp = True
            while startUp:
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
                        startUp = False
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