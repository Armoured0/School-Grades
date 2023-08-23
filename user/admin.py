import program.database as database

class Admin:
    def __init__(self, userName, password) -> None:
        self.userName = userName
        self.password = password
    
    def passwordCheck(self):
        usrPassword = input("Enter admin password: ")
        
        if usrPassword == self.password:
            return True
        else:
            print("Credentials incorrect!")
            return False
        
    def adminCheck():
        loggingIn = True
        
        while loggingIn:
            
            usrInput = input("Enter admin username: ")
            admin = Admin.createAdminInstance(usrInput)
            
            if admin:
                checkResult = admin.passwordCheck()
                return checkResult
        
    def createAdminInstance(userName):
        connection = database.createConnection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM admins WHERE userName = ?", (userName,))
        adminDbData = cursor.fetchall()
        connection.close()
        
        if adminDbData:
            adminInfo = adminDbData[0]
            return Admin(adminInfo[0], adminInfo[1])
        else:
            print("Username not found!")
            return False
        
    def saveAdminData(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO admins VALUES (?,?)", (self.userName, self.password))
        
        connection.commit()
        connection.close()
        
    def createNewAdmin():
        choosingSave = True
        creatingAdmin = True
        
        while creatingAdmin:
            userNameCheck = True
            userName = input("Select a username for your admin account: ")
            
            if userName == "STOP":
                userNameCheck = False
            
            connection = database.createConnection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT userName FROM admins")
            adminAccounts = cursor.fetchall()
            
            connection.close()
            
            for userDBName in adminAccounts:
                if userDBName[0] == userName:
                    userNameCheck = False

            if userNameCheck:
                userPassword = input("Select a password for your admin account: ")

                self = Admin(userName, userPassword)

                print(f"Your username is: {self.userName}.\n"
                    f"Your password is: {self.password}")
                creatingAdmin = False
                
            else:
                print("Username already taken or reserved. Please select another.")
                    

        while choosingSave:
            usrInput = input("Would you like to save this account? Y or N: ")
            
            if usrInput.upper() == "Y":
                choosingSave = False
                self.saveAdminData()
            
            elif usrInput.upper() == "N":
                choosingSave = False
            
            else:
                print("Invalid option!")
                pass
      
    def deleteAdminRecord(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE from admins WHERE userName = ?", (self.userName,))
        connection.commit()
        connection.close()
       
    def manageAdminAccounts():
        connection = database.createConnection()
        cursor = connection.cursor()
        usingMenu = True
        
        while usingMenu:
            print("Choose an option:\n"
                "1. Create admin accounts.\n"
                "2. View all admin accounts.\n"
                "3. Delete admin accounts.\n"
                "4. Exit")
            usrInput = input("Enter here: ")
            
            if usrInput == "1":
                Admin.createNewAdmin()
                
            elif usrInput == "2":
                accountNumber = 0
                cursor.execute("SELECT userName FROM admins")
                adminAccounts = cursor.fetchall()
                
                print ("---- Admin Accounts ----")
                
                for account in adminAccounts:
                    accountNumber += 1
                    print(f"{accountNumber}. {account[0]}")
                    
                print ("----------------")
            
            elif usrInput == "3":
                selectingAccount = True
                
                while selectingAccount:
                    rmAdminUsrName = input("Enter username of account for removal, enter 'STOP' to cancel.\nEnter here: ")

                    if rmAdminUsrName == "STOP":
                        selectingAccount = False
                        print ("----------------")
                        
                    elif rmAdminUsrName == "default":
                        selectingAccount = False
                        print("Unable to delete default user.")
                        print ("----------------")
                        
                    else:
                        selectedAdminAccount = Admin.createAdminInstance(rmAdminUsrName)
                        
                        if selectedAdminAccount:
                            selectingAccount = False
                            selectedAdminAccount.deleteAdminRecord()
                            
                            print("Account deleted!")
                            print ("----------------")
                            
                        else:
                            print("Invalid username, try again.")

            elif usrInput == "4":
                choosing = True
                
                while choosing:
                    print("Are you sure you want to exit?")
                    usrInput = input("Enter here (Y/N): ")
                    
                    if usrInput.upper() == "Y":
                        usingMenu = False
                        choosing = False
                        
                    elif usrInput.upper() == "N":
                        choosing = False
                        
                    else:
                        print("Invalid option!")
            else:
                print("Invalid option!")
        
        connection.close()
      
    def resetAdminData():
        resettingData = True
        
        while resettingData:
            print("Are you sure you want to reset all admin data?")
            usrInput = input("Enter here (Y/N): ")
            
            if usrInput.upper() == "Y" or usrInput.upper() == "N":
                
                if usrInput.upper() == "Y":
                    connection = database.createConnection()
                    cursor = connection.cursor()
                    
                    cursor.execute("DROP TABLE admins")
                    connection.close()
                    
                    database.establishTable()
                    
                    print("All admin data has been reset!")
                    resettingData = False
                
                if usrInput.upper() == "N":
                    print("Exiting!")
                    resettingData = False
            
            else:
                print("Invalid option!")
                pass
       
if __name__ == '__main__':
    print("Please run the main script!")