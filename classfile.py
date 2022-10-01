class Student:
    def __init__(self, id, firstName, lastName, age, maths=None, english=None,
                 physics=None, business=None, computerScience=None, latin=None):
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
    
    @classmethod
    def construct(self, studentDataBase):
        return self(studentDataBase[0], studentDataBase[1],
                    studentDataBase[2], studentDataBase[3],
                    studentDataBase[4], studentDataBase[5],
                    studentDataBase[6], studentDataBase[7],
                    studentDataBase[8], studentDataBase[9])

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
        
class Admin:
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
    @classmethod
    def construct(self, studentDataBase):
        return self(studentDataBase[0], studentDataBase[1])
    def passwordCheck(self, usrPassword):
        if usrPassword == self.password:
            return True
        else:
            return False
        
        
if __name__ == '__main__':
    print("Please run the main script!")
