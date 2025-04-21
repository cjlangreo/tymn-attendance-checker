import sqlite3

# Database
conn = sqlite3.connect("src/gui/test.db")
cursor = conn.cursor()