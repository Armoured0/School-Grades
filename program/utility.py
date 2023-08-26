def yesOrNo(question):
    choosing = True
    while choosing == True:
        print("----------------")
        userChoice = input(f"{question}\nEnter here (Y/N): ")
        
        if (userChoice.upper() == "Y"):
            choosing = False
            return True
        elif (userChoice.upper() == "N"):
            choosing = False
            return False
        else:
            print("Invalid choice, please try again!")
            
if __name__ == '__main__':
    print("Please run the main script!")