import sqlite3

schema = open("sqlite_database_creation.sql", "r", encoding="utf-8").read()  # or paste the SQL string here

conn = sqlite3.connect("exportaciones.db")
conn.executescript(schema)
conn.commit()
conn.close()
