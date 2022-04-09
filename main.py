import pickle

from classfile import Student


def createStudent():
    firstName = input("What is the student's first name?")
    lastName = input("What is the student's last name?")
    studentAge = input("How old is the student?")

    student = Student(firstName, lastName, studentAge)

    print(f"This student is called {student.fullName()}.\n"
          f"They are {student.age} years old.")
    return student

def saveStudentData(student):
    try:
        with open('idCount.txt', 'r') as idCount:
            id = idCount.read()
        with open(f'{id}', 'wb') as f:
            pickle.dump(student, f)

        with open(f'{id}', 'rb') as r:
            student = pickle.load(r)
            print(f"{student.fullName()} has been saved at {id}")

        with open('idCount.txt', 'w') as idCount:
            id = int(id) + 1
            idCount.write(str(id))
    except:
        print("Save failed.")
        pass

mainRunning = True
print("Welcome to student data!")

while mainRunning:
    startUp = True
    while startUp:
        try:
            print("Please select an option:\n"
                "1. Create new student.\n"
                "2. Edit student data.\n"
                "3. Access student data.")
            usrInput = int(input("Choose your option: "))
            if usrInput >= 1 and usrInput <= 3:
                startUp = False
                pass
            else:
                print("Invalid option!")
                pass

        except ValueError:
            print("Invalid option!")
            pass

    if usrInput == 1:
        choosingSave = True
        student = createStudent()
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
        
    elif usrInput == 2:
        pass
    elif usrInput == 3:
        pass
    