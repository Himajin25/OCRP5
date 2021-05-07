from Classes import *

purecoco = Database()
purecoco.connect_to_server()
purecoco.connect_to_database()
purecoco.build_tables()
data = purecoco.fetch_data()
purecoco.populate_tables(data)
program = 1
while program:
    main()
purecoco.end_connection()