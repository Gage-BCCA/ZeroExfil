import sqlite3


class TestDatabaseFunctionality:

    def test_connection_to_db(self):
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM links")
        assert results.fetchall() != []

import requests
res = requests.post('http://localhost:5000/api/secure_link', json={"url": "https://google.com","password":"12345"})
if res.ok:
    print(res.json())

    # IOILTN9MD

res2 = requests.post('http://localhost:5000/api/unlock_link', json={"id": "IOILTN9MD","password":"12345"})
if res2.ok:
    print(res2.json())