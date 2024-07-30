import csv
import links


def write_link_to_csv(link: links.Link) -> None:
    """ Writes an entry to the links csv file. Takes a link object as input and returns None."""
    with open('links.csv', 'a') as datafile:
        writer = csv.writer(datafile, delimiter=",")
        writer.writerow(link.get_link_data())
    return None


def find_link(link_id: str) -> links.Link:
    """ Finds an entry in the links csv by the unique ID. Returns the link if found. If no link is found, returns None."""
    with open('links.csv', 'r') as datafile:
        reader = csv.reader(datafile, delimiter=",")
        for row in reader:
            if row[1] == link_id:
                link = links.Link(original_url=row[0], 
                                 new_url=row[1], 
                                 password=row[2],
                                 )
                return link
        else:
            return None



def fetch_datafile_rows() -> int:
    """ Returns the number of rows currently in the datafile. """
    with open('links.csv', 'r') as datafile:
        reader = csv.reader(datafile, delimiter=",")
        return sum(1 for row in reader)