# PURCOCO app, _your best cocompanion_ !

With this program, you can find **healthier** substitutes to your coco products based on their nutritional scores. 
You can save the substitutes in your favorites and check them out later at your convienience !

The database is build from products from **OpenFoodFacts** and organized in categories.


## PREREQUISITES:
> this program was built using python 3.6.9 on WSL(Ubuntu) and MySQL 8.0

- **Python 3.6.9** or more recent;

- **MySQL 8.0** or more recent running and a user created with full rights on 'PurcocoDB' database.


## INSTALLATION :

1. Clone this project from [github](https://github.com/Himajin25/OCRP5.git) or download the zip file on your computer.   
    (see this [cloning tutorial](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for guidance)

2. Create a virtual environment with python3. 
    1. In terminal, go to the root of of the app directory and run **python3 -m venv purcoco_venv**
    2. Activate your virtual environment, run the following in terminal:
        - (WINDOWS)**purcoco_venv\Scripts\activate.bat** 
        - (UNIX) **purcoco_venv/bin/activate**

3. Enter **pip install -r requirements.txt** to install required modules;

4. Store your credentials securely:
    1. Create a file named **.env** in the root of your directory 
    2. Type the following on the first 2 lines: 
        > USER='_your MySQL username_'   
        > PASSWORD='_your MySQL password_'
    3. Save your file 

5. Run **python3 init.py** to (re)build the database and populate the tables

6. Run **python3 purcoco.py** to enjoy the app!


## USE:

- To select an entry in a menu, enter the corresponding number in terminal and press Enter;

- Follow the instructions on the screen!

## RESET:

- Your saved items list can be reset from within the app's _Favorites Menu_

- Simply rerun **python3 init.py** to rebuild the whole database from scratch;



Enjoy coconut in a healthier way!