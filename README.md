# Welcome to **purcoco** app !

With this program, you can find **healthier** substitutes to your coco products based on their nutritional scores. 
You can save the substitutes in your favorites and check them out at your convienience !

The database is build with products from **OpenFoodFacts** and organized in categories.


## iNSTALLATION PREREQUISITES:

-> **Python 3.6.9** or more recent;

-> **MySQL 8.0** or more recent running and a user created with fullrights on 'PurcocoDB' database


## INSTALLATION :

1. Clone this project from [github](https://github.com/Himajin25/OCRP5.git) or download the zip file on your computer.
    (see this [cloning tutorial](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for guidance)

2. Create a virtual environment with python3 :
        - Run  **python3 -m virtualenv purcoco** in the terminal while in the directory you'll use;
        - Run **.\Scripts\activate** 

3. Enter **pip3 install -r requirements.txt** to install required modules;
    - Windows :
    - Linux :

4. Store your credentials securely:
    1. Create a file named **.env** in your directory 
    2. Type the following on the first 2 lines: 
        > USER='_your MySQL username_'
        > PASSWORD='_your MySQL password_'
    3. Save your file 

5. Run **init.py** to (re)build the database and populate the tables
    - Windows :
    - Linux :

6. Run **purcoco.py** to enjoy the app!
    - Windows :
    - Linux :



## USE:

- To select an option, enter corresponding number in terminal and press enter;

- Follow the instructions on the screen!

## RESET:

- Your saved items list can be reset from within the app;

- Simply rerun init.py to rebuild the whole database from scratch;




Enjoy coconut in a healthier way!