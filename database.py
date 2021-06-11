import config as c
from mysql.connector import connect, Error, errorcode
import requests


class Database:
    """ Class that handles all database operations """

    def __init__(self):
        self.user = c.MYSQL_USER_NAME
        self.password = c.MYSQL_PASSWORD
        self.database = c.DATABASE
        self.config = {'user': self.user, 'password': self.password, 'database': c.DATABASE}
        self.cnx = connect(**self.config)
        self.cursor = self.cnx.cursor(buffered=True)

    def connect_to_server(self):
        """ Connects to MySQL server while checking user name and password for errors  """

        try:
            config = {'user': self.user, 'password': self.password}
            cnx = connect(**config)
            self.connection = cnx
            self.cursor = cnx.cursor(buffered=True)
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            else:
                print(e)
        else:
            print(f'{self.user} connected succesfully to MYSQL and {c.DATABASE} database')

    def connect_to_database(self):
        """ Connects to database and creates it if it doesn't exists """

        create_db_query = f"CREATE DATABASE IF NOT EXISTS {c.DATABASE} DEFAULT CHARACTER SET utf8mb4"
        use_db_query = f"USE {c.DATABASE}"
        try:
            self.cursor.execute(create_db_query)
            print(f"db {c.DATABASE} created succesfully")
        except Error as e:
            print(f"DB {c.DATABASE} creation failed")
            print(e)
        else:
            self.cursor.execute(use_db_query)
            print(f"db {c.DATABASE} selected")
            self.connection.commit()
            print("changes committed")

    def build_tables(self):
        """ Build the tables from the TABLES dictionary in the constants.py file """

        for table_name in c.TABLES:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"table {table_name} dropped")

        for table_name in c.TABLES:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            table = c.TABLES[table_name]
            self.cursor.execute(table)
            print('table {} created'.format(table_name))

    def fetch_data(self):
        """ Fetches the data for the tables from the openfood facts API """

        products_list_data = []
        for category in c.CATEGORIES:
            url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
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
                except (KeyError, AssertionError):
                    pass

                else:
                    products_list_data.append((code, cat_name, name, brand, stores, nutrition_grades, url))

        return products_list_data

    def populate_tables(self, data):
        """ Uses the fetched data and inserts it in the tables """

        cat_data = list(enumerate(c.CATEGORIES, 1))
        feed_products_query = "INSERT IGNORE INTO Products (code, cat_name, name, brand, stores, nutri_grade, url)\
                                 VALUES (%s, %s, %s, %s, %s, %s, %s)"
        feed_categories_query = "INSERT IGNORE INTO Category (id, name) VALUES (%s, %s)"
        self.cursor.executemany(feed_products_query, data)
        self.cursor.executemany(feed_categories_query, cat_data)
        self.connection.commit()
        print('tables populating succesfully completed')

    def get_products_from_category(self, category_selection):
        """ Displays the products from the user selected category """

        show_products_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s"
        show_products_params = (c.CATEGORIES[category_selection-1],)
        self.cursor.execute(show_products_query, show_products_params)
        products_selection = self.cursor.fetchall()
        return products_selection

    def get_healthier_products(self, selected_product_id):
        """ Proposes healthier alternatives compared to the user selected product """

        product_nutri_category_query = "SELECT nutri_grade, cat_name FROM Products where id = %s"
        product_nutri_category_params = (selected_product_id,)
        self.cursor.execute(product_nutri_category_query, product_nutri_category_params)
        product_nutri_and_category = self.cursor.fetchone()
        product_nutri = product_nutri_and_category[0]
        product_category = product_nutri_and_category[1]
        print(f"Your product nutriscore  is << {product_nutri} >> and its category is << {product_category} >>")

        show_healthier_query = "SELECT name, brand, nutri_grade, id FROM Products where cat_name = %s \
                                and nutri_grade < %s ORDER BY nutri_grade"
        show_healthier_params = (product_category, product_nutri)
        self.cursor.execute(show_healthier_query, show_healthier_params)
        healthier_products = self.cursor.fetchall()
        return healthier_products

    def display_favorites(self):
        """ Displays the products saved by the user into the favorites table """

        display_favorites_query = "SELECT cat_name, name, brand, nutri_grade, id FROM Products\
                                     INNER JOIN Favorites ON Products.id = Favorites.product_id"
        self.cursor.execute(display_favorites_query)
        saved_items = self.cursor.fetchall()
        return saved_items

    def save_to_favorites(self, healthy_choice_id):
        """ Proposes to save selected product replacement to favorites table """

        save_to_favorites_query = "REPLACE into Favorites (product_id) SELECT id FROM Products where id = %s"
        save_to_favorites_params = (healthy_choice_id,)
        self.cursor.execute(save_to_favorites_query, save_to_favorites_params)
        print(f"product with id {healthy_choice_id} succesfully added to favorites")
        self.cnx.commit()

    def erase_favorites(self):
        """ Allows for reset of favorites table """

        table = c.TABLES['Favorites']
        self.cursor.execute("DELETE FROM Favorites")
        # self.cursor.execute("DROP TABLE IF EXISTS Favorites")
        self.cursor.execute(table)
        self.cnx.commit()

    def end_connection(self):
        """ Terminates the connection to the server and closes the cursor """
        self.cursor.close()
        self.connection.close()
        print('connection terminated')
