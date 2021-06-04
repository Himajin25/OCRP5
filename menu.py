import sys
from os import system, name


class Menu:
    """ Class that handles the user interface, allows for user to navigate menus """

    def __init__(self, title, about, options):
        self.title = title
        self.about = about 
        self.options = options
        self.instructions = "HOW TO USE: Choose an option, enter its corresponding number and press Enter"

    def clear_screen(self):
        """ Clears the terminal screen upon change of menu """

        # for windows 
        if name == 'nt': 
            _ = system('cls') 
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 
            
    def display(self):
        """ This method handles the appearance of the different menus """
        self.clear_screen()
        print(" ", "_"*150)
        print("|"," "*150, "|")
        print("|", " "*55, f"<< {self.title} >>")
        print("|", " "*30, f"{self.instructions}")
        print("|", "_"*150, "|")
        print("|", " "*150, "|")
        print("|", "0", "|", "Navigation Menu (go to << MAIN MENU >> or Quit app)")
        print("|","="*150, "|")
        print("|", " ", "|", f"{self.about}")
        for i, r in enumerate(self.options, 1):
            print("|","-"*150, "|")
            print("|", i, "|", r)
        print("|","_"*150, "|" )

    def user_input(self):
        """ This method allows for the user to select elements from numbered lists by entering a number"""

        try :
            print()
            user_choice = int(input("What is your selection?\n( Enter 0 to navigate app ) \n"))
            assert user_choice in range(len(self.options)+1)
        except:
            ValueError, AssertionError
            print("INVALID INPUT - Try again: ")
            return self.user_input()
        else :
            
            if user_choice == 0:
                self.menu_navigation()
            else:
                return user_choice

    def menu_navigation(self):
        """ This method allows to return to main menu or quit the application when user enters '0'  """
        self.clear_screen()
        print(" ", "_"*150)
        print("|"," "*150, "|")
        print("|", " "*55, "<< NAVIGATION MENU >>")
        print("|", "_"*150, "|")

        navigation = input("- enter 'm' to return to main menu\n- enter 'q' to quit program:\n ").lower()
        print(f"You selected <<{navigation}>>")
      
        if navigation == 'm':
            print('returning to main menu')
            from main import main
            main()
           

        elif navigation == 'c':
            print('cancelling navigation')
            return
                    
        elif navigation == 'q':
            print('exiting program')  
            sys.exit()          
                        
        else:
            print('enter valid input')
            Menu.menu_navigation(self) 

