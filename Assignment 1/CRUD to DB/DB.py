import sqlite3

connection = sqlite3.connect('Tasks.db')
table = connection.cursor()

table.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN
    )''')