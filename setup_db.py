import sqlite3

conn = sqlite3.connect('helpdesk.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
             username TEXT PRIMARY KEY, 
             password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS tickets (
             id INTEGER PRIMARY KEY AUTOINCREMENT, 
             user TEXT, 
             issue TEXT, 
             status TEXT)''')

conn.commit()
conn.close(
