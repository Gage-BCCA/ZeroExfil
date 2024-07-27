import datetime
import string
import random

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

if __name__ == "__main__":
    test_object = Link("test", "test2", "12345")
    print(test_object)
    print(test_object.new_url)
    print(test_object.original_url)
    print(test_object.metadata)
    print(test_object.metadata.views)