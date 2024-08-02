import datetime
import string
import random
from flask_scrypt import check_password_hash, generate_password_hash, generate_random_salt
import csv

class Link:

    def __init__(self, original_url: str, new_url: str, password: str):
        self.original_url = original_url
        self.new_url = new_url
        self.password = password
        self.metadata = self.create_metadata()

    def __str__(self):
        return self.new_url
    
    def create_metadata(self):
        metadata = Metadata(0, datetime.datetime.now(), 0, "scrypt")
        return metadata
    
    def get_link_data(self) -> list:
        return [self.original_url, self.new_url, self.password]
    

class Metadata:

    def __init__(self, views: int, date_created: datetime.datetime, age: int, encryption: str):
        self.views = views
        self.date_created = date_created
        self.age = age
    
    def __str__(self):
        return f"Metadata Object with {self.views} views, created on {self.date_created}"



def generate_random_string(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def verify_id_uniqueness(new_url: str) -> bool:
    """ Used during creation of a new link ID to ensure that it is unique. """
    with open('links.csv', 'r') as datafile:
        reader = csv.reader(datafile, delimiter=",")
        for row in reader:
            if row[1] == new_url:
                return False
        else:
            return True

def create_link(url: str, password: str) -> Link:

    # Password Salting and Hashing
    salt = generate_random_salt()
    pwd_hash = generate_password_hash(password, salt)
    pwd_and_hash = pwd_hash + b"$" + salt

    # New URL Generation
    new_path = generate_random_string()
    while not verify_id_uniqueness(new_path):
        new_path = generate_random_string()

    link_object = Link(original_url=url, 
                                new_url=new_path, 
                                password=pwd_and_hash.decode(), # We have to decode this here to make sure the "b" does not get added to the byte string
                                 )
    return link_object
