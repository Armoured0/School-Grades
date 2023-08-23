import program.database as database
import program.utility as utility

class Student:
    def __init__(self, id, firstName, lastName, age, maths=None, english=None,
                 physics=None, business=None, computerScience=None, latin=None) -> None:
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.maths = maths
        self.english = english
        self.physics = physics
        self.business = business
        self.computerScience = computerScience
        self.latin = latin
        
    def saveStudentData(self, idChange=False):
        connection = database.createConnection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM students ORDER BY id")
        studentIds = cursor.fetchall()
        
        update = False
        for id in studentIds:
            if id[0] == self.id:
                update = True

        if update == True:
            cursor.execute("""UPDATE students SET firstName = ?, lastName = ?, age = ?, mathsGrade = ?,
                            englishGrade = ?, physicsGrade = ?, businessGrade= ?, computerScienceGrade = ?,
                            latinGrade = ? WHERE id = ?""", (self.firstName, self.lastName, self.age,
                            self.maths, self.english, self.physics, self.business, self.computerScience,
                            self.latin, self.id))
        
        elif idChange:
            cursor.execute("""UPDATE students SET id = ? WHERE id = ?""", (self.id, self.id+1))
        
        else:
            cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
            (self.id, self.firstName, self.lastName, self.age, self.maths,
                self.english, self.physics, self.business, self.computerScience,
                self.latin))

        connection.commit()
        print("----------------")
        print(f"Data saved at student ID: {self.id}")
        connection.close()
        
    def createStudentAccount():
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
            
        self = Student(studentId, firstName, lastName, studentAge)

        print(f"This student is called {self.fullName()}.\n"
            f"They are {self.age} years old.")
        
        if utility.yesOrNo("Would you like to save this student?") == True:
            self.saveStudentData()
        
    def editStudentData(self):
        editing = True
        try:
            
            while editing:
                print("What do you want to edit?\n"
                      "1. Name\n"
                      "2. Age")
                usrInput = int(input("Enter here: "))
                
                if usrInput == 1:
                    print(f"Student's name is currently {self.fullName()}")
                    self.firstName = input("What is the students first name? ")
                    self.lastName = input("What is the students last name? ")
                    self.saveStudentData()
                    
                elif usrInput == 2:
                    print(f"Student's age is currently {self.age}")
                    self.age = input("What is the students age? ")
                    self.saveStudentData()
                else:
                    print("Invalid option!")
                    
                if utility.yesOrNo("Would you like to continue editing student credentials?") == False:
                    editing = False
                        
        except ValueError:
            print("Invalid option!")
            
    def changeStudentGrade():
        enteringGrade = True
        while enteringGrade:
            usrInput = int(input("Enter grade (0-100): "))
            if usrInput >= 0 and usrInput <= 100:
                enteringGrade = False
                return usrInput
            else:
                print("Invalid percentage!")
                
    def deleteStudentRecord(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (self.id,))
        connection.commit()
        cursor.execute("SELECT id from students")
        studentIds = cursor.fetchall()
        for id in studentIds:
            if id[0] > self.id:
                student = Student.createStudentInstance(id[0])
                student.id = student.id - 1
                student.saveStudentData(idChange=True)
        connection.close()
            
    def addStudentGrades(self):
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
                    self.maths = Student.changeStudentGrade()
                    self.saveStudentData()

                elif usrInput == 2:
                    print("Enter your english grade as a percentage.")
                    self.english = Student.changeStudentGrade()
                    self.saveStudentData()
                    
                elif usrInput == 3:
                    print("Enter your physics grade as a percentage.")
                    self.physics = Student.changeStudentGrade()
                    self.saveStudentData()
                    
                elif usrInput == 4:
                    print("Enter your business grade as a percentage.")
                    self.business = Student.changeStudentGrade()
                    self.saveStudentData()
                    
                elif usrInput == 5:
                    print("Enter your computer science grade as a percentage.")
                    self.computerScience = Student.changeStudentGrade()
                    self.saveStudentData()
                    
                elif usrInput == 6:
                    print("Enter your latin grade as a percentage.")
                    self.latin = Student.changeStudentGrade()
                    self.saveStudentData()
                            
                else:
                    print("Invalid option!")
            
                if utility.yesOrNo("Would you like to continue editing this student's grades?") == False:
                    choosingGrade = False
                    
        except ValueError:
            print("Invalid option!")
            
    def savedStudents():
        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id")
        students = cursor.fetchall()
        connection.close()
        
        if students:
            print("----------------")
            print("Avaliable students:")
            for student in students:
                student = Student.createStudentInstance(student[0])
                print(f"ID: {student.id}. Full name: {student.fullName()}")
            return True
        else:
            print("No avaliable students")
            return False
            
    def accessStudentData():
        searchingForStudent = True
        exiting = False
        accessingData = True
        while accessingData:
            while searchingForStudent:
                try:
                    print("----------------\n"
                        "How would you like to find your student?\n"
                        "1. View all available students.\n"
                        "2. Search for student by name.\n"
                        "3. Exit")
                    usrInput = int(input("Choose your option: "))

                    if usrInput == 1:
                        if Student.savedStudents():
                            searchingForStudent = False
                        else:
                            searchingForStudent = False
                            accessingData = False
                            exiting = True

                    elif usrInput == 2:
                        studentName = input("Enter name of student: ")
                        matches = database.studentSearch(studentName)
                        if matches:
                            print("----------------\nMatching students accounts:")
                            for student in matches:
                                student = Student.createStudentInstance(student[0])
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
                print("----------------\nEnter the ID of the student profile you would like to access.")
                id = input("Enter here: ")
                student = Student.createStudentInstance(id)
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
                                student.editStudentData()
                            if usrInput == 2:
                                student.addStudentGrades()
                            if usrInput == 3:
                                choosing = True
                                
                                while choosing:
                                    print("Are you sure you want to delete this account?")
                                    usrInput = input("Enter here (Y/N): ")
                                    
                                    if usrInput.upper() == "Y":
                                        student.deleteStudentRecord()
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
            
    def createStudentInstance(id):
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
        
    def resetStudentData():
        userResponse = utility.yesOrNo("Are you sure you want to reset all student data?")
        
        if userResponse == True:
            connection = database.createConnection()
            cursor = connection.cursor()
            cursor.execute("DROP TABLE students")
            connection.close()
            database.establishTable()
                
            print("All student data has been reset!")
        
        elif userResponse == False:
            print("Exiting!")

    
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
    
    def letterGrade(self, gradePercent):
        try:
            if int(gradePercent) <= 40:
                return "E"
            elif int(gradePercent) <= 50:
                return "D"
            elif int(gradePercent) <= 60:
                return "C"
            elif int(gradePercent) <= 70:
                return "B"
            elif int(gradePercent) <= 80:
                return "A"
            elif int(gradePercent) > 80:
                return "A*"
        except TypeError:
            return "None"
        
if __name__ == '__main__':
    print("Please run the main script!")