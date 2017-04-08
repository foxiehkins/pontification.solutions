import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE urls(id INTEGER PRIMARY KEY, url TEXT, len TEXT, pontification TEXT)
''')
db.commit()
