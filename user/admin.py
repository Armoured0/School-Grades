if __name__ == '__main__':
    print("Please run the main script!")
else:
    import program.database as database
    import program.utility as utility

class Admin:
    def __init__(self, userName, password) -> None:
        self.userName = userName
        self.password = password
    
    #* admin creation subroutines
    
    def createNewAdmin():
        creatingAdmin = True
        
        while creatingAdmin:
            print("----------------")
            userNameCheck = True
            userName = input("Select a username for your admin account: ")
            
            if (userName == "STOP"):
                userNameCheck = False
            
            connection = database.createConnection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT userName FROM admins")
            adminAccounts = cursor.fetchall()
            
            connection.close()
            
            for userDBName in adminAccounts:
                if (userDBName[0] == userName):
                    userNameCheck = False

            if (userNameCheck == True):
                userPassword = input("Select a password for your admin account: ")

                self = Admin(userName, userPassword)
                print("----------------")
                print(f"Selected username: {self.userName}.\n"
                    f"Selected password: {self.password}")
                creatingAdmin = False
                
            else:
                print("Username already taken or reserved. Please select another.")
                    
        if (utility.yesOrNo("Would you like to save this account? Y or N: ") == True):
            self.saveAdminData()
    
    
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
            print("Account not found!")
            return False
        
        
    def saveAdminData(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO admins VALUES (?,?)", (self.userName, self.password))
        print(f"Data saved on admin account '{self.userName}'")
        
        connection.commit()
        connection.close()
            
    
    #* admin data access/manipulation
    
    
    def manageAdminAccounts():
        connection = database.createConnection()
        cursor = connection.cursor()
        usingMenu = True
        
        while usingMenu:
            print("----------------")
            print("Please select an option:\n"
                "1. Create admin accounts.\n"
                "2. View all admin accounts.\n"
                "3. Delete admin accounts.\n"
                "4. Exit\n"
                "----------------")
            
            usrInput = input("Enter here: ")
            
            if (usrInput == "1"):
                Admin.createNewAdmin()
                
            elif (usrInput == "2"):
                accountNumber = 0
                cursor.execute("SELECT userName FROM admins")
                adminAccounts = cursor.fetchall()
                
                print ("----------------\n*Admin Accounts*")
                
                for account in adminAccounts:
                    accountNumber += 1
                    print(f"{accountNumber}. {account[0]}")
                    
            
            elif (usrInput == "3"):
                selectingAccount = True
                while selectingAccount:
                    print("----------------")
                    rmAdminUsrName = input("Enter username of account for removal, enter 'STOP' to cancel.\nEnter here: ")

                    if (rmAdminUsrName == "STOP"):
                        selectingAccount = False
                        
                    elif (rmAdminUsrName == "default"):
                        selectingAccount = False
                        print("Unable to delete default user.")
                        
                    else:
                        selectedAdminAccount = Admin.createAdminInstance(rmAdminUsrName)
                        
                        if (selectedAdminAccount):
                            selectingAccount = False
                            selectedAdminAccount.deleteAdminRecord()
                            
                            print("Account deleted!")

            elif (usrInput == "4"):
                choosing = True
                
                while choosing:
                    print("Are you sure you want to exit?")
                    usrInput = input("Enter here (Y/N): ")
                    
                    if (usrInput.upper() == "Y"):
                        usingMenu = False
                        choosing = False
                        
                    elif (usrInput.upper() == "N"):
                        choosing = False
                        
                    else:
                        print("Invalid option!")
            else:
                print("Invalid option!")
        
        connection.close()
    
    
    def deleteAdminRecord(self):
        connection = database.createConnection()
        cursor = connection.cursor()
        cursor.execute("DELETE from admins WHERE userName = ?", (self.userName,))
        connection.commit()
        connection.close()
        
        
    def resetAdminData():
        userResponse = utility.yesOrNo("Are you sure you want to reset all admin data?")
        
        if (userResponse == True):
            connection = database.createConnection()
            cursor = connection.cursor()
            cursor.execute("DROP TABLE admins")
            connection.close()
            database.establishTable()
                
            print("All admin data has been reset!")
        
        elif userResponse == False:
            print("Exiting!")

    
    #* admin utility
    
    
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