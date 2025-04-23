import sqlite3

fakedb_path = "src/gui/test.db"
# Database
def connect_db():
  return sqlite3.connect(fakedb_path)