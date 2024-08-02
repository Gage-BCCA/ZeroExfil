import requests
import csv_utils
import links


class TestAPIFunctions:

    def test_secure_url(self):
        res = requests.post('http://localhost:5000/api/secure_link', json={"url": "https://google.com","password":"12345"})
        if res.ok:
            assert res.json()
    
    def test_unlock_url(self):
        res2 = requests.post('http://localhost:5000/api/unlock_link', json={"id": "IOILTN9MD","password":"12345"})
        if res2.ok:
            assert res2.json()["url"] == "https://google.com"
    
    def test_fetch_datafile_rows(self):
        res3 = requests.get('http://localhost:5000/api/database_info')
        if res3.ok:
            assert int(res3.json()["rowcount"]) >= 0


class TestCsvUtilFunctions:

    def test_find_link(self):
        link = csv_utils.find_link("IOILTN9MD")
        assert link.get_link_data != []


class TestLinkFunctions:

    def test_link_creation(self):
        link = links.create_link("https://google.com", "12345")
        assert link.get_link_data != []
    