class Student:
    def __init__(self, firstName, lastName, age):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
