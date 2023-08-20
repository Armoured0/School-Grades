def exitProgram():
    choosing = True
    
    while choosing:
        print("Are you sure you want to exit?")
        usrInput = input("Enter here (Y/N): ")
        
        if usrInput.upper() == "Y":
            print("Exiting...")
            exit()
        
        elif usrInput.upper() == "N":
            choosing = False
       
        else:
            print("Invalid option!")

if __name__ == '__main__':
    print("Please run the main script!")