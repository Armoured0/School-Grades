
# Stops imports if run as main script
if __name__ == '__main__':
    print("Please run the main script!")
else:
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
        
    #* student creation subroutines
    
    def createStudentAccount():
        gettingStudentInfo = True
        while gettingStudentInfo:
            try:
                firstName = input("Enter student's first name: ")
                lastName = input("Enter student's last name: ")
                studentAge = int(input("Enter student age: "))
            except ValueError:
                print("Invalid input!")
            else:
                gettingStudentInfo = False

        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM students ORDER BY id")
        allStudentIds = cursor.fetchall()
        connection.close()
        
        if (allStudentIds):
            studentId = allStudentIds[-1][0]+1
        else:
            studentId = 0
            
        self = Student(studentId, firstName, lastName, studentAge)

        print("----------------")
        print(f"This student is called {self.fullName()}.\n"
            f"They are {self.age} years old.")
        
        if (utility.yesOrNo("Would you like to save this student?") == True):
            self.saveStudentData()
    
    
    def saveStudentData(self, idChange=False):
        connection = database.createConnection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM students ORDER BY id")
        studentIds = cursor.fetchall()
        
        update = False
        for id in studentIds:
            if (id[0] == self.id):
                update = True

        if update == True and idChange == False:
            cursor.execute("""UPDATE students SET firstName = ?, lastName = ?, age = ?, mathsGrade = ?,
                            englishGrade = ?, physicsGrade = ?, businessGrade= ?, computerScienceGrade = ?,
                            latinGrade = ? WHERE id = ?""", (self.firstName, self.lastName, self.age,
                            self.maths, self.english, self.physics, self.business, self.computerScience,
                            self.latin, self.id))
        
        #* idChange parameter used to decrease all student ids above deleted entry
        elif idChange:
            cursor.execute("""UPDATE students SET id = ? WHERE id = ?""", (self.id-1, self.id))
        
        else:
            cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
            (self.id, self.firstName, self.lastName, self.age, self.maths,
                self.english, self.physics, self.business, self.computerScience,
                self.latin))

        connection.commit()
        if idChange == False:
            print("----------------")
            print(f"Data saved at student ID: {self.id}")
        connection.close()
    
            
    def createStudentInstance(id):
        connection = database.createConnection()
        cursor = connection.cursor()
            
        cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
        studentDbData = cursor.fetchall()
        connection.close()
            
        if (studentDbData):
            studentInfo = studentDbData[0]
            return Student(studentInfo[0], studentInfo[1], studentInfo[2], 
                        studentInfo[3], studentInfo[4], studentInfo[5], 
                        studentInfo[6], studentInfo[7], studentInfo[8], 
                        studentInfo[9])
        else:
            print("Invalid student ID!")
            return None
    
    
    #* student access/data manipulation
    
                    
    def accessStudentData():
        searchingForStudent = True
        
        while searchingForStudent:
            studentsFound = False
            print("----------------\n"
                "How would you like to find your student?\n"
                "1. View all available students.\n"
                "2. Search for student by name.\n"
                "3. Exit\n"
                "----------------")
            usrInput = input("Choose your option: ")

            if (usrInput == "1"):
                if (Student.savedStudents()):
                    studentsFound = True
 
            elif (usrInput == "2"):
                studentName = input("Enter name of student: ")
                matches = database.studentSearch(studentName)
                if (matches):
                    print("----------------\nMatching students accounts:")
                    for student in matches:
                        student = Student.createStudentInstance(student[0])
                        print(f"ID: {student.id}. Full name: {student.fullName()}.")

                    studentsFound = True
                else:
                    print("No matches found!")
            
            elif (usrInput == "3"):
                searchingForStudent = False
                                    
            else:
                print("Invalid option!")
                
            if studentsFound == True:
                print("----------------")
                print("Input ID of profile to view, input 'STOP' to cancel")
                studentId = input("Enter here: ")
                if (studentId.upper() != "STOP"):
                    studentInstance = Student.createStudentInstance(studentId)
                    if (studentInstance):
                        studentInstance.studentProfile()
          
                
    def studentProfile(self):
        usingProfile = True
        while usingProfile:
            print(f"---- Student Profile ----\n"
                f"ID: {self.id}\n"
                f"Name: {self.fullName()}\n"
                f"Age: {self.age}\n"
                "---- Student Grades -----\n"
                f"Maths - {self.letterGrade(self.maths)}\n"
                f"English - {self.letterGrade(self.english)}\n"
                f"Physics - {self.letterGrade(self.physics)}\n"
                f"Business - {self.letterGrade(self.business)}\n"
                f"Computer Science - {self.letterGrade(self.computerScience)}\n"
                f"Latin - {self.letterGrade(self.latin)}\n"
                "-------- Options --------\n"
                "1. Edit Credentials\n"
                "2. Add/Edit Grades\n"
                "3. Delete Profile\n"
                "4. Exit Menu")

            usrInput = input("Enter here: ")


            if (usrInput == "1"):
                self.editStudentData()
                
            elif (usrInput == "2"):
                self.addStudentGrades()
                
            elif (usrInput == "3"):                
                userResponse = utility.yesOrNo("Are you sure you want to delete this account?")
                
                if (userResponse == True):
                    self.deleteStudentRecord()
                    print("Account deleted!")
                    usingProfile = False
                    
            elif (usrInput == "4"):
                usingProfile = False
            
            else:
                print("Invalid option!")


    def editStudentData(self):
        editing = True
        while editing:
            selectionComplete = False
            print("----------------\n"
                  "What do you want to edit?\n"
                    "1. Name\n"
                    "2. Age\n"
                    "----------------")
            usrInput = input("Enter here: ")
            print("----------------")
            
            if (usrInput == "1"):
                print(f"Student's name is currently {self.fullName()}")
                self.firstName = input("Enter student's first name: ")
                self.lastName = input("Enter student's last name: ")
                self.saveStudentData()
                selectionComplete = True
                
            elif (usrInput == "2"):
                try:
                    print(f"Student's age is currently {self.age}")
                    self.age = int(input("What is the students age? "))
                    self.saveStudentData()
                except ValueError:
                    print("Invalid input!")
                else:
                    selectionComplete = True

            else:
                print("Invalid option!")

            if (selectionComplete ==  True):
                if (utility.yesOrNo("Would you like to continue editing student credentials?") == False):
                    editing = False


    def addStudentGrades(self):
        choosingGrade = True
        while choosingGrade:
            selectionComplete = False
            print("----------------\n"
                "Please select a subject to edit:\n"
                "1. Maths\n"
                "2. English\n"
                "3. Physics\n"
                "4. Business\n"
                "5. Computer Science\n"
                "6. Latin\n"
                "----------------")

            usrInput = input("Choose your option: ")
            print("----------------")
            
            if (usrInput == "1"):
                print("Enter your math grade as a percentage.")
                self.maths = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True

            elif (usrInput == "2"):
                print("Enter your english grade as a percentage.")
                self.english = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True
                
            elif (usrInput == "3"):
                print("Enter your physics grade as a percentage.")
                self.physics = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True
                
            elif (usrInput == "4"):
                print("Enter your business grade as a percentage.")
                self.business = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True
                
            elif (usrInput == "5"):
                print("Enter your computer science grade as a percentage.")
                self.computerScience = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True
                
            elif (usrInput == "6"):
                print("Enter your latin grade as a percentage.")
                self.latin = Student.inputStudentGrade()
                self.saveStudentData()
                selectionComplete = True
                        
            else:
                print("Invalid option!")
        
            if (selectionComplete == True):
                if (utility.yesOrNo("Would you like to continue editing this student's grades?") == False):
                    choosingGrade = False


    def deleteStudentRecord(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (self.id,))
        connection.commit()
        
        cursor.execute("SELECT id from students")
        studentIds = cursor.fetchall()
        for id in studentIds:
            if (id[0] > self.id):
                studentInstance = Student.createStudentInstance(id[0])
                studentInstance.saveStudentData(idChange=True)
                
        connection.close()
        
        
    def resetStudentData():
        userResponse = utility.yesOrNo("Are you sure you want to reset all student data?")
        
        if (userResponse == True):
            connection = database.createConnection()
            cursor = connection.cursor()
            cursor.execute("DROP TABLE students")
            connection.close()
            database.establishTable()
                
            print("All student data has been reset!")
        
        elif userResponse == False:
            print("Exiting!")
    
    
    #* student utility subroutines
    
    
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
            print("----------------")
            print("No students in database!")
            return False
    
    
    def inputStudentGrade():
        enteringGrade = True
        while enteringGrade:
            usrInput = int(input("Enter grade (0-100): "))
            if (usrInput >= 0 and usrInput <= 100):
                enteringGrade = False
                return usrInput
            else:
                print("Invalid percentage!")
        
        
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
    
    
    def letterGrade(self, gradePercent):
        try:
            if (gradePercent <= 40):
                return "E"
            elif (gradePercent <= 50):
                return "D"
            elif (gradePercent <= 60):
                return "C"
            elif (gradePercent <= 70):
                return "B"
            elif (gradePercent <= 80):
                return "A"
            elif (gradePercent > 80):
                return "A*"
        except TypeError:
            return "None"