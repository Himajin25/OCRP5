from classes import *


purcoco = Database()
purcoco.connect_to_server()
purcoco.connect_to_database()
purcoco.build_tables()
data = purcoco.fetch_data()
purcoco.populate_tables(data)
program = 1

while program:
    main()
purcoco.end_connection()