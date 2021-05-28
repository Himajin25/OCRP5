from dotenv import load_dotenv
load_dotenv()
import os


""" Constants used in the purcoco app """

USER_NAME = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")

DATABASE = "PurcocoDB"
CATEGORIES = ["eaux de coco", "lait de coco", "huile de coco", "yaourts a la noix de coco", "sablés à la noix de coco", "chips de noix de coco séchée", "farine de noix de coco séchée", "sucres de coco"]
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