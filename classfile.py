class Student:
    def __init__(self, firstName, lastName, age, maths, english):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.maths = maths
        self.english = english
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
