from os import system, name
import time
import constants as c
import menu
 
from Database import Database


""" Classes, methods and functions used to build the purcoco app """


main_menu = ['Search Product to Replace', 'View Saved Products']
about_main_menu = "MENU NAME"
about_categories_menu = "CATEGORY NAME"
about_products_display = "('PRODUCT NAME', 'BRAND', 'NUTRISCORE', 'DATABASE ID')"


""" This < Database > class handles all database operations """


def clear_screen():
    """ This function clears the terminal screen upon change of menu """

    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



def title_menu():
    """ This function builds the main menu and handles user input """

    clear_screen()
    title_menu = menu.Menu("MAIN MENU", about_main_menu, main_menu)
    title_menu.display()
    title_menu_selection = title_menu.user_input()
    return title_menu_selection

def categories_menu():
    """ This function builds the category menu and handles the user input """

    clear_screen()
    categories_menu = menu.Menu("CATEGORIES MENU", about_categories_menu, c.CATEGORIES)
    categories_menu.display()
    category_selection = categories_menu.user_input()
    return category_selection

def products_menu(category_selection):
    """ This function builds the products menu and handles user input """

    clear_screen()
    show_products = purcoco.get_products_from_category(category_selection)
    products_menu = menu.Menu("PRODUCTS MENU",about_products_display, show_products)
    products_menu.display()
    product_selection = products_menu.user_input()
    selected_product_id = show_products[product_selection-1][3]
    print(f"selected product id is {selected_product_id}")
    return selected_product_id

def healthy_menu(product_selection):
    """ This function builds the healthy alternatives menu and handles user input """

    clear_screen()
    show_healthier_products = purcoco.get_healthier_products(product_selection)
    healthier_menu = menu.Menu("HEALTHIER OPTIONS MENU", about_products_display, show_healthier_products)
    healthier_menu.display()
    if len(show_healthier_products) == 0:
        print("No better option found")
        time.sleep(4)
        healthier_menu.menu_navigation()
    else:
        healthy_choice = healthier_menu.user_input()
        healthy_choice_id = show_healthier_products[healthy_choice-1][3]
        print("You selected ", show_healthier_products[healthy_choice-1])
        return healthy_choice_id

def save_to_favorites_menu(healthy_choice_id):
    """ This function displays prompt for user to choose and confirm whether to save healthier product to favorites table """

    save_to_favorites_prompt = input("Save to your favorites?\n - Enter 'y' to add to favorites;\n - Enter 'n' to go back to selection;\n").lower()
    if save_to_favorites_prompt == "y":
        purcoco.save_to_favorites(healthy_choice_id)
    elif save_to_favorites_prompt == "n":
        pass
    else :
        print("INVALID INPUT\nEnter 'y' or 'n'")
        save_to_favorites_menu(healthy_choice_id)

def favorites_menu():
    """ This function builds the favorites menu and displays saved product to user """

    clear_screen()
    show_favorites = purcoco.display_favorites()
    favorites_menu_init= menu.Menu('FAVORITES MENU', about_products_display, show_favorites)
    favorites_menu_init.display()
    erase_favorites_prompt()
    favorites_menu_init.menu_navigation()

def erase_favorites_prompt():
    """ This function prompt the user to reset the favorites table """

    while True:
        erase_favorites_prompt = input("- enter 'e' to erase your saved products;\n- enter 'c' to continue:\n").lower()
        if erase_favorites_prompt == 'e':
            while True:
                erase_favorites_confirmation = input("- You are about to erase your saved products\n - Enter 'y' to confirm\n - Enter 'n' to return to favorites\n").lower()
                if erase_favorites_confirmation == 'y':
                    purcoco.erase_favorites()
                    print("< Favorites > erased, resest completed")
                    return
                elif erase_favorites_confirmation == 'n':
                    print(" reset cancelled... returning to << FAVORITES MENU >>")
                    return favorites_menu()
                else: 
                    print('INVALID INPUT')
                    pass
        elif erase_favorites_prompt == 'c':
            break
        else: 
            print("INVALID INPUT\n")
            pass

def replace_item():
    """ This function handles the prompts and inputs if user chooses to look for a porduct to replace """

    choosen_category = categories_menu()
    choosen_product = products_menu(choosen_category)
    choosen_replacement = healthy_menu(choosen_product)
    save_to_favorites_menu(choosen_replacement)

def app():
    """ This function is the main function to launch the user interface and start the program """
    user_choice = title_menu()
    if user_choice == 1:
        replace_item()
    elif user_choice == 2:
        favorites_menu()

purcoco = Database()

