from database import Database
from menu import Menu
import config as c
import time


class Controller:

    main_menu = ['Search Product to Replace', 'View Saved Products']
    about_main_menu = "MENU NAME"
    about_categories_menu = "CATEGORY NAME"
    about_products_display = "('PRODUCT NAME', 'BRAND', 'NUTRISCORE', 'DATABASE ID')"
    about_favorites_display = "('CATEGORY', 'PRODUCT NAME', 'BRAND', 'NUTRISCORE', 'DATABASE ID')"

    def __init__(self):
        self.database = Database()

    def title_menu(self):

        title_menu = Menu("MAIN MENU", self.about_main_menu, self.main_menu)
        title_menu.clear_screen()
        title_menu.display()
        title_menu_selection = title_menu.user_input()
        return title_menu_selection

    def categories_menu(self):
        """ Builds the category menu and handles the user input """

        categories_menu = Menu("CATEGORIES MENU", self.about_categories_menu, c.CATEGORIES)
        categories_menu.clear_screen()
        categories_menu.display()
        category_selection = categories_menu.user_input()
        return category_selection

    def products_menu(self, category_selection):
        """ Builds the products menu and handles user input """

        show_products = self.database.get_products_from_category(category_selection)
        products_menu = Menu("PRODUCTS MENU", self.about_products_display, show_products)
        products_menu.clear_screen()
        products_menu.display()
        product_selection = int(products_menu.user_input())
        selected_product_id = show_products[product_selection-1][3]
        print(f"selected product id is {selected_product_id}")
        return selected_product_id

    def healthy_menu(self, product_selection):
        """ Builds the healthy alternatives menu and handles user input """

        show_healthier_products = self.database.get_healthier_products(product_selection)
        healthier_menu = Menu("HEALTHIER OPTIONS MENU", self.about_products_display, show_healthier_products)
        healthier_menu.clear_screen()
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

    def save_to_favorites_menu(self, healthy_choice_id):
        """ Displays prompt for user to choose and confirm whether to save healthier product to favorites table """

        save_to_favorites_prompt = input("\nSave to your favorites?\n- Enter 'y' to add to favorites;\n"
                                         "- Enter 'n' to go back to selection;\n").lower()
        if save_to_favorites_prompt == "y":
            self.database.save_to_favorites(healthy_choice_id)
        elif save_to_favorites_prompt == "n":
            pass
        else:
            print("INVALID INPUT\nEnter 'y' or 'n'")
            self.save_to_favorites_menu(healthy_choice_id)

    def favorites_menu(self):
        """ Builds the favorites menu and displays saved product to user """

        show_favorites = self.database.display_favorites()
        favorites_menu = Menu('FAVORITES MENU', self.about_favorites_display, show_favorites)
        favorites_menu.clear_screen()
        favorites_menu.display()
        while True:
            erase_favorites_prompt = input("- enter 'e' to erase your saved products;\n"
                                           "- enter '0' to navigate app\n").lower()
            if erase_favorites_prompt == '0':
                favorites_menu.menu_navigation()
            elif erase_favorites_prompt == 'e':
                while True:
                    erase_favorites_confirmation = input("- You are about to erase your saved products\n"
                                                         "- Enter 'y' to confirm\n"
                                                         "- Enter 'n' to return to favorites\n").lower()
                    if erase_favorites_confirmation == 'y':
                        self.database.erase_favorites()
                        print("< Favorites > erased, resest completed")
                        return
                    elif erase_favorites_confirmation == 'n':
                        print(" reset cancelled... returning to << FAVORITES MENU >>")
                        return self.favorites_menu()
                    else:
                        print('INVALID INPUT')
                        pass
            else:
                print("INVALID INPUT\n")
                pass

    def replace_item(self):
        """ Handles the prompts and inputs if user chooses to look for a porduct to replace """

        choosen_category = self.categories_menu()
        choosen_product = self.products_menu(choosen_category)
        choosen_replacement = self.healthy_menu(choosen_product)
        self.save_to_favorites_menu(choosen_replacement)

    def run(self):

        while True:

            """ Launches the user interface and start the program """
            user_choice = self.title_menu()
            if user_choice == 1:
                self.replace_item()
            elif user_choice == 2:
                self.favorites_menu()
