import sqlite3

# Membuat koneksi ke database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Membuat tabel users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()
