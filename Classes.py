from mysql.connector import connect, Error, errorcode
import requests
import sys
from os import system, name
import time
from constants import *
from purecoco import purecoco

main_menu = ['Search Product to Replace', 'View Saved Products']
about_main_menu = "MENU NAME"
about_categories_menu = "CATEGORY NAME"
about_products_display = "('PRODUCT NAME', 'BRAND', 'NUTRISCORE', 'DATABASE ID')"

class Database:

    user = None
    password = None
    connection = None
    cursor = None

    def __init__(self):
        self.user = USER
        self.password = PASSWORD
        self.database = DATABASE

    def connect_to_server(self):

        try:
            config = {'user' : self.user, 'password' : self.password}
            cnx = connect(**config)
            self.connection = cnx
            self.cursor = cnx.cursor(buffered=True)
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print ('Something is wrong with your user name or password')
            else:
                print (e)
        else:
            print(f'{self.user} connected succesfully to MYSQL and {DATABASE} database')

    def connect_to_database(self):
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {DATABASE} DEFAULT CHARACTER SET utf8mb4"
        use_db_query = f"USE {DATABASE}"
        try: 
            self.cursor.execute(create_db_query)
            print(f"db {DATABASE} created succesfully")
        except Error as e:
            print(f"DB {DATABASE} creation failed")
            print(e)
        else : 
            self.cursor.execute(use_db_query)
            print(f"db {DATABASE} selected")
            self.connection.commit()
            print("changes committed")
        
    def build_tables(self):
        # with self.cursor as cursor:
        for table_name in TABLES:
            if table_name is not 'Favorites':
                self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"table {table_name} dropped")

        for table_name in TABLES:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            table = TABLES[table_name]
            self.cursor.execute(table)
            print('table {} created'.format(table_name))
    
    def fetch_data(self):
        products_list_data = []
        for category in CATEGORIES:
            url= 'https://fr.openfoodfacts.org/cgi/search.pl?'
            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": category,
                "page_size": "200",
                "json": 1
                }
            r = requests.get(url, params=params)
            text = r.json()

            for i in range(len(text["products"])):
                try:
                    cat_name = category
                    code = text["products"][i]["code"]
                    name = text["products"][i]["product_name"]
                    brand = text["products"][i]["brands"]
                    stores = text["products"][i]["stores"]
                    nutrition_grades = text["products"][i]["nutrition_grade_fr"]
                    url = text["products"][i]["url"]
                    keys = [code, cat_name, name, brand, stores, nutrition_grades, url]
                    for key in keys: 
                        assert len(str(key)) > 0
                except:
                    (KeyError, AssertionError)
                    pass

                else: 
                    products_list_data.append((code, cat_name, name, brand, stores, nutrition_grades, url))
        print(products_list_data)
        return products_list_data

    def populate_tables(self, data):
        cat_data = list(enumerate(CATEGORIES, 1))
        feed_products_query = "INSERT IGNORE INTO Products (code, cat_name, name, brand, stores, nutri_grade, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        feed_categories_query =  "INSERT IGNORE INTO Category (id, name) VALUES (%s, %s)"
        self.cursor.executemany(feed_products_query, data)
        self.cursor.executemany(feed_categories_query, cat_data)
        self.connection.commit()
        print('tables populating succesfully completed')

    def end_connection(self):
        self.cursor.close()
        self.connection.close()
        print('connection terminated')
    
    # @staticmethod
    def get_products_from_category(self, category_selection):
        show_products_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s"
        show_products_params = (CATEGORIES[category_selection-1],)
        self.cursor.execute(show_products_query, show_products_params)
        products_selection = self.cursor.fetchall()
        return products_selection
    
    def get_healthier_products(self, selected_product_id):
        product_nutri_category_query = "SELECT nutri_grade, cat_name FROM Products where id = %s"
        product_nutri_category_params = (selected_product_id,)
        self.cursor.execute(product_nutri_category_query, product_nutri_category_params)
        product_nutri_and_category = self.cursor.fetchone()
        product_nutri = product_nutri_and_category[0]
        product_category = product_nutri_and_category[1]
        print(f"Your product nutriscore  is << {product_nutri} >> and its category is << {product_category} >>")

        show_healthier_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s and nutri_grade < %s ORDER BY nutri_grade"
        show_healthier_params = (product_category, product_nutri)
        self.cursor.execute(show_healthier_query, show_healthier_params)
        healthier_products = self.cursor.fetchall()
        return healthier_products


    def display_favorites(self):
        display_favorites_query = "SELECT name, brand, nutri_grade, id FROM Products INNER JOIN Favorites ON Products.id = Favorites.product_id"
        self.cursor.execute(display_favorites_query)
        saved_items = self.cursor.fetchall()
        return saved_items

    def save_to_favorites(self, healthy_choice_id):
        save_to_favorites_query = "REPLACE into Favorites (product_id) SELECT id FROM Products where id = %s"
        save_to_favorites_params = (healthy_choice_id,)
        self.cursor.execute(save_to_favorites_query, save_to_favorites_params)
        print(f"product with id {healthy_choice_id} succesfully added to favorites")
        self.connection.commit()

    def erase_favorites(self):
        table = TABLES['Favorites']
        self.cursor.execute("DROP TABLE IF EXISTS Favorites")
        self.cursor.execute(table)
        self.connection.commit()
        
            


class Menu:
    def __init__(self, title, about, options):
        self.title = title
        self.about = about 
        self.options = options
        self.instructions = "HOW TO USE: Choose an option, enter its corresponding number and press Enter"

    def display(self):
        print(" ", "_"*150)
        print("|"," "*150, "|")
        print("|", " "*55, f"<< {self.title} >>")
        print("|", " "*30, f"{self.instructions}")
        #print("|"," "*100, "|")
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
        try :
            print()
            user_choice = int(input("What is your selection?\n( Enter 0 to navigate app ) \n"))
            assert user_choice in range(len(self.options)+1)
        except:
            ValueError, AssertionError
            print("INVALID INPUT - Try again: ")
            return Menu.user_input(self)
        else :
            if user_choice == 0:
                Menu.menu_navigation(self)
            else:
                return user_choice

    def menu_navigation(self):
        clear_screen()
        print(" ", "_"*150)
        print("|"," "*150, "|")
        print("|", " "*55, "<< NAVIGATION MENU >>")
        print("|", "_"*150, "|")

        navigation = input("- enter 'm' to return to main menu\n- enter 'q' to quit program:\n ").lower()
        print(f"You selected <<{navigation}>>")
      
        if navigation == 'm':
            print('returning to main menu')
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
    

print ("Always executed")
 
if __name__ == "__main__":
    print ("Executed when invoked directly")
else:
    print ("Executed when imported")
    


def clear_screen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


def title_menu():
    clear_screen()
    title_menu = Menu("MAIN MENU", about_main_menu, main_menu)
    title_menu.display()
    title_menu_selection = title_menu.user_input()
    return title_menu_selection

def categories_menu():
    clear_screen()
    categories_menu = Menu("CATEGORIES MENU", about_categories_menu, CATEGORIES)
    categories_menu.display()
    category_selection = categories_menu.user_input()
    return category_selection

def products_menu(category_selection):
    clear_screen()
    show_products = purecoco .get_products_from_category(category_selection)
    products_menu = Menu("PRODUCTS MENU",about_products_display, show_products)
    products_menu.display()
    product_selection = products_menu.user_input()
    selected_product_id = show_products[product_selection-1][3]
    print(f"selected product id is {selected_product_id}")
    return selected_product_id

def healthy_menu(product_selection):
    clear_screen()
    show_healthier_products = purecoco.get_healthier_products(product_selection)
    healthier_menu = Menu("HEALTHIER OPTIONS MENU", about_products_display, show_healthier_products)
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

    save_to_favorites_prompt = input("Save to your favorites?\n - Enter 'y' to add to favorites;\n - Enter 'n' to go back to selection;\n").lower()
    if save_to_favorites_prompt == "y":
        purecoco.save_to_favorites(healthy_choice_id)
    elif save_to_favorites_prompt == "n":
        pass
    else :
        print("INVALID INPUT\nEnter 'y' or 'n'")
        save_to_favorites_menu(healthy_choice_id)

def favorites_menu():
    clear_screen()
    show_favorites = purecoco .display_favorites()
    favorites_menu_init= Menu('FAVORITES MENU', about_products_display, show_favorites)
    favorites_menu_init.display()
    erase_favorites_prompt()
    favorites_menu_init.menu_navigation()

def erase_favorites_prompt():
    while True:
        erase_favorites_prompt = input("- enter 'e' to erase your saved products;\n- enter 'c' to continue:\n").lower()
        if erase_favorites_prompt == 'e':
            while True:
                erase_favorites_confirmation = input("- You are about to erase your saved products\n - Enter 'y' to confirm\n - Enter 'n' to return to favorites\n").lower()
                if erase_favorites_confirmation == 'y':
                    purecoco.erase_favorites()
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
    choosen_category = categories_menu()
    choosen_product = products_menu(choosen_category)
    choosen_replacement = healthy_menu(choosen_product)
    save_to_favorites_menu(choosen_replacement)

def main():
    user_choice = title_menu()
    if user_choice == 1:
        replace_item()
    elif user_choice == 2:
        favorites_menu()

