import program.database as database
import program.menu as menu
from user.admin import Admin
from user.student import Student

def main():
    database.establishTable()
    print("You must login to access this application.")
    if Admin.adminCheck() == True:
        mainRunning = True
        print("Login successful!")
        print("Welcome to the student database!")
        while mainRunning:
            print("----------------\n"
                "Please select an option:\n"
                "1. Create new student.\n"
                "2. Access and edit student data.\n"
                "3. Reset student data.\n"
                "4. Manage admin accounts.\n"
                "5. Reset admin data.\n"
                "6. Exit program.\n"
                "----------------")
            usrInput = input("Choose your option: ")
            if usrInput == "1":
                Student.createStudentAccount()
            elif usrInput == "2":
                Student.accessStudentData()
            elif usrInput == "3":
                Student.resetStudentData()
            elif usrInput == "4":
                Admin.manageAdminAccounts()
            elif usrInput == "5":
                Admin.resetAdminData()
            elif usrInput == "6":
                menu.exitProgram()
            else:
                print("Invalid option!")
                    
            
if __name__ == '__main__':
    main()