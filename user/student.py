import program.database as database

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