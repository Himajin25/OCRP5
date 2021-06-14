import os


MYSQL_USER_NAME = os.environ.get('USER')
MYSQL_PASSWORD = os.environ.get('PASSWORD')

DATABASE = "PurcocoDB"

CATEGORIES = ['Eaux De Coco', 'Lait De Coco', 'Huile De Coco',
              'Yaourts A La Noix De Coco', 'Sablés À La Noix De Coco',
              'Chips De Noix De Coco Séchée', 'Farine De Noix De Coco Séchée', 'Sucres De Coco']

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
