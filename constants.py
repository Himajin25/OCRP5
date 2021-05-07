
from mysql.connector import connect, Error, errorcode
import requests
import sys
from os import system, name


def clear():
    # for windows 
    
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
    print(name)

config = { 
    'user' : 'root',
    'password' :'My5QL N1c0',
}

DATABASE = 'dbtest9'
try:
    with connect(**config) as cnx:
        print(cnx)
        cursor = cnx.cursor(buffered=True)
except Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('check credentials')
        exit()
    else: 
        print(e)
        print('try connecting again after solving problem')
        exit()



db_creation = "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8mb4".format(DATABASE)
db_use = "USE {}".format(DATABASE)

cnx.reconnect()

def use_db():
    cursor.execute(db_use)
    print(f"database {DATABASE} succesfully selected")

def create_and_connect_to_db():
    try: 
        cursor.execute(db_creation)
        print('db {} created succesfully'.format(DATABASE))
    except Error as e:
        print("DB {} creation failed".format(DATABASE))
        print(e)
    else : 
        cursor.execute(db_use)
        print('db {} selected'.format(DATABASE))

try: 
    use_db()
except Error as e:
    create_and_connect_to_db()

TABLES = {}

TABLES['Products'] = (
    "CREATE TABLE IF NOT EXISTS `Products` ("
    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
    "  `code` varchar(100) NOT NULL,"
    "  `cat_name` varchar(40) NOT NULL,"
    "  `name` varchar(100) NOT NULL,"
    "  `brand` varchar(100) NOT NULL,"
    "  `stores` varchar(100) NOT NULL,"
    "  `nutri_grade` char(1) NOT NULL,"
    "  `url` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=INNODB")

TABLES['Category'] = (
    "CREATE TABLE IF NOT EXISTS `Category` ("
	"   `id` SMALLINT NOT NULL,"
	"   `name` varchar(100) NOT NULL,"
	"   PRIMARY KEY (`id`)"
    ") ENGINE=INNODB")

TABLES['Favorites'] = (
    "CREATE TABLE IF NOT EXISTS `Favorites` ("
	"   `product_id` SMALLINT NOT NULL,"
    "   PRIMARY KEY (`product_id`),"
    "   CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Products (id)"
    ") ENGINE=INNODB")
    
for table_name in TABLES:
    if table_name != 'Favorites':
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        print('table {} dropped'.format(table_name))

for table_name in TABLES:
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    table = TABLES[table_name]
    cursor.execute(table)
    print('table {} created'.format(table_name))



CATEGORIES = ["eaux de coco", "lait de coco", "huile de coco", "creme de coco", "sucres de coco", "Yaourts a la noix de coco"]

prods = []
for category in CATEGORIES:
    
    query= 'https://fr.openfoodfacts.org/cgi/search.pl?'
    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": category,
        "page_size": "100",
        "json": 1
        }
    r = requests.get(query, params=params)
 
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
            for e in keys: 
                assert len(str(e)) > 0
        except:
            (KeyError, AssertionError)
            pass

        else: 
            prods.append((code, cat_name, name, brand, stores, nutrition_grades, url))


print(prods)

cat_data = list(enumerate(CATEGORIES, 1))
   

add_data = "INSERT IGNORE INTO Products (code, cat_name, name, brand, stores, nutri_grade, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
add_cat =  "INSERT IGNORE INTO Category (id, name) VALUES (%s, %s)"
cursor.executemany(add_data, prods)
cursor.executemany(add_cat, cat_data)
cnx.commit()

show_favorites_query = "SELECT * FROM Favorites"
with cnx.cursor() as cursor:
    cursor.execute(show_favorites_query)
    favorites_selection = cursor.fetchall()
    
    for i, r in enumerate(favorites_selection, 1):
        print(i, "-", r)

main_menu = ['Search Product to Replace', 'View Saved Products']
about_main_menu = "MENU NAME"
about_categories_menu = "CATEGORY NAME"
about_products_display = "('PRODUCT NAME', 'BRAND', 'NUTRISCORE', 'DATABASE ID')"




class Menu:
    def __init__(self, title, about, choices):
        self.title = title
        self.about = about 
        self.choices = choices
        self.instructions = "HOW TO USE: Choose an option, enter its corresponding number and press Enter"

    def display(self):
        print(" ", "_"*102)
        print("|"," "*100, "|")
        print("|", " "*35, f"<< {self.title} >>")
        print("|", " "*2, f"{self.instructions}")
        #print("|"," "*100, "|")
        print("|", "_"*100, "|")
        print("|", " "*100, "|")
        print("|", "0", "|", "Navigation Menu (go to << MAIN MENU >> or Quit app)")
        print("|","="*100, "|")
        print("|", " ", "|", f"{self.about}")
        for i, r in enumerate(self.choices, 1):
            print("|","-"*100, "|")
            print("|", i, "|", r)
        print("|","_"*100, "|" )

    def user_input(self):
        try :
            print()
            user_choice = int(input("What is your selection?\n( Enter 0 to navigate app ) \n"))
            assert user_choice in range(len(self.choices)+1)

        except:
            ValueError, AssertionError
            print("INVALID INPUT\nEnter valid input: ")
            return Menu.user_input(self)
        else :
            if user_choice == 0:
                Menu.menu_navigation(self)
                
            else:
                return user_choice

    def menu_navigation(self):
        print(" ","_"*50)
        print("|"," "*50, "|")
        print(" "*15, "<< NAVIGATION MENU >>")
        print("|","_"*50,"|")
        print(" "*52)
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

        
        
def display_favorites():
    display_favorites_query = "SELECT name, brand, nutri_grade, id FROM Products INNER JOIN Favorites ON Products.id = Favorites.product_id"
    with cnx.cursor() as cursor:
        cursor.execute(display_favorites_query)
        saved_items = cursor.fetchall()
        return saved_items

def title_menu():
    clear()
    title_menu = Menu("MAIN MENU", about_main_menu, main_menu)
    title_menu.display()
    title_menu_selection = title_menu.user_input()
    return title_menu_selection

def erase_favorites():
    erase_favorites_prompt = input("- enter 'e' to erase your saved products;\n- enter 'c' to continue:\n").lower()
    while True:
        if erase_favorites_prompt == 'e':
            erase_favorites_confirmation = input("- You are about to erase your saved products\n - Enter 'y' to confirm\n - Enter 'n' to return to favorites\n").lower()
            if erase_favorites_confirmation == 'y':
                with cnx.cursor() as cursor:
                    cursor.execute("DROP TABLE IF EXISTS Favorites")
                    cursor.execute(table)
                    cnx.commit()
                    print("< Favorites > erased, resest completed")
                    return
            elif erase_favorites_confirmation == 'n':
                print(" reset cancelled... returning to << FAVORITES MENU >>")
                return favorites_menu()
            else: 
                print('INVALID INPUT')
                continue
        elif erase_favorites_prompt == 'c':
            break
        else: 
            print("INVALID INPUT\n")
            return erase_favorites()

def favorites_menu():
    clear()
    show_favorites = display_favorites()
    favorites_menu_init= Menu('FAVORITES MENU', about_products_display, show_favorites)
    favorites_menu_init.display()
    erase_favorites()
    favorites_menu_init.menu_navigation()

def categories_menu():
    clear()
    categories_menu = Menu("CATEGORIES MENU", about_categories_menu, CATEGORIES)
    categories_menu.display()
    category_selection = categories_menu.user_input()
    return category_selection

def products_menu(category_selection):
    clear()
    show_products = get_products_from_category(category_selection)
    products_menu = Menu("PRODUCTS MENU",about_products_display, show_products)
    products_menu.display()
    product_selection = products_menu.user_input()
    selected_product_id = show_products[product_selection-1][3]
    print(f"selected product id is {selected_product_id}")
    return selected_product_id
    
def healthy_menu(product_selection):
    clear()
    show_healthier_products = get_healthier_products(product_selection)
    healthier_menu = Menu("HEALTHIER OPTIONS MENU", about_products_display, show_healthier_products)
    healthier_menu.display()
    if len(show_healthier_products) == 0:
        print("No better option found")
        healthier_menu.menu_navigation()
    else:
        healthy_choice = healthier_menu.user_input()
        healthy_choice_id = show_healthier_products[healthy_choice-1][3]
        print("You selected ", show_healthier_products[healthy_choice-1])
        return healthy_choice_id

def save_to_favorites_menu(healthy_choice_id):

    save_to_favorites_prompt = input("Save to your favorites?\n - Enter 'y' to add to favorites;\n - Enter 'n' to go back to selection;\n").lower()
    if save_to_favorites_prompt == "y":
        save_to_favorites_query = "REPLACE into Favorites (product_id) SELECT id FROM Products where id = %s"
        save_to_favorites_params = (healthy_choice_id,)
        with cnx.cursor() as cursor:
            cursor.execute(save_to_favorites_query, save_to_favorites_params)
            print(f"product with id {healthy_choice_id} succesfully added to favorites")
            cnx.commit()

    elif save_to_favorites_prompt == "n":
        pass
    else :
        print("INVALID INPUT\nEnter 'y' or 'n'")
        save_to_favorites_menu(healthy_choice_id)

    
def get_products_from_category(category_selection):
    show_products_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s"
    show_products_params = (CATEGORIES[category_selection-1],)
    with cnx.cursor() as cursor:
        cursor.execute(show_products_query, show_products_params)
        products_selection = cursor.fetchall()
        return products_selection

def get_healthier_products(selected_product_id):
    product_nutri_category_query = "SELECT nutri_grade, cat_name FROM Products where id = %s"
    product_nutri_category_params = (selected_product_id,)
    with cnx.cursor() as cursor:
        cursor.execute(product_nutri_category_query, product_nutri_category_params)
        product_nutri_and_category = cursor.fetchone()
        product_nutri = product_nutri_and_category[0]
        product_category = product_nutri_and_category[1]
        print(f"Your product nutriscore  is << {product_nutri} >> and its category is << {product_category} >>")

    show_healthier_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s and nutri_grade < %s ORDER BY nutri_grade"
    show_healthier_params = (product_category, product_nutri)
    with cnx.cursor() as cursor:
        cursor.execute(show_healthier_query, show_healthier_params)
        healthier_products = cursor.fetchall()
        return healthier_products

def replace_item():
        choosen_category = categories_menu()
        choosen_product = products_menu(choosen_category)
        choosen_replacement = healthy_menu(choosen_product)
        save_to_favorites_menu(choosen_replacement)

def main():
    choosen_action = title_menu()
    if choosen_action == 1:
        replace_item()
    elif choosen_action == 2:
        favorites_menu()
        
program = 1
while program:
    main()
