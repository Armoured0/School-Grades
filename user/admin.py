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