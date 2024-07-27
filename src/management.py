import sqlite3

def create_sqlite_database(filename):
    """ create a SQLite database and create tables using the schema file """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        with open('schema.sql') as fp:
            conn.executescript(fp.read()) 
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_sqlite_version() -> str:
    return sqlite3.sqlite_version

if __name__ == '__main__':
    create_sqlite_database("links.db")
