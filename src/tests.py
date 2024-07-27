import sqlite3


class TestDatabaseFunctionality:

    def test_connection_to_db(self):
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM links")
        assert results.fetchall() != []
