from database import Database

purcoco = Database()
purcoco.connect_to_server()
purcoco.connect_to_database()
purcoco.build_tables()
data = purcoco.fetch_data()
purcoco.populate_tables(data)
purcoco.end_connection()
