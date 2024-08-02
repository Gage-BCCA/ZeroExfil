import os
import csv
import csv_utils

FILE_NAME = 'links.csv'

def build_app_datafile() -> None:
    # Create csv database file if it doesn't exist
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["original_url", "id", "password", "date_created"])
        print(f"{FILE_NAME} has been created.")
    else:
        print(f"{FILE_NAME} already exists.")
        print(f"{FILE_NAME} currently has {csv_utils.fetch_datafile_rows()} rows.")

def clear_app_datafile() -> None:
    if os.path.isfile(FILE_NAME):
        os.remove(FILE_NAME)

if __name__ == "__main__":
    clear_app_datafile()
    build_app_datafile()

