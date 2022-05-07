class Student:
    def __init__(self, firstName, lastName, age, maths, english):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.maths = maths
        self.english = english
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
    def letterGrade(self, gradePercent):
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
        
class Admin:
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
    def passwordCheck(self, usrPassword):
        if usrPassword == self.password:
            return True
        else:
            return False
        
        
if __name__ == '__main__':
    print("Please run the main script!")
