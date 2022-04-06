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




student = createStudent()
saveStudentData(student)
