# user.py
import csv

def validate_user(username, password, filepath="./data/Credentials.csv"):
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'].strip() == username and row['password'].strip() == password:
                    return row['role'].strip()  # Return role if credentials match
    except FileNotFoundError:
        print("Credential file not found.")
    return None  # Return None if no match or file is missing
