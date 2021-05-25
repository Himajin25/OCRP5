Purcoco App

Welcome to purcoco's application !

With this program, you can select a coconut product and find a healthier substitute based on its nutritional score. You can save the substitute in your favorites and check it a your convienience !

The database is build with products from OpenFoodFacts and organized in categories.


iNSTALLATION PREREQUISITES:

-> Python 3.6.9 or more recent;

-> MySQL 8.0 or more recent running and a user created with fullrights on 'PurcocoDB' database


INSTALLATION :

-> Clone this project from github (https://github.com/Himajin25/OCRP5.git) or download zip file on your computer.
    (see https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository for guidance)

-> Create a virtual environment with python3 :
        - enter  'python3 -m virtualenv purcoco ' in the terminal while in the directory you'll use;
        - enter ' .\Scripts\activate '

-> Enter ' pip3 install -r requirements.txt ' to install required modules;

-> Edit config.py by replacing 'YourUserName' and 'YourPassword' with your own credentials between brackets;

-> Run init.py to (re)build the database and populate the tables;

-> Run purcoco.py to enjoy the app!


USE:

-> To select an option, enter corresponding number in terminal and press enter;

-> Follow the instructions on the screen!

RESET:

-> Your saved items list can be reset from within the app;

-> Simply rerun init.py to rebuild the whole database from scratch;




Enjoy coconut in a healthier way!