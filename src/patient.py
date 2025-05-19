import csv
import random
import datetime
from tkinter import simpledialog, messagebox  # Added messagebox for error alerts

class PatientManager:
    def __init__(self, filepath):  # Initialize with the file path and load existing records
        self.filepath = filepath
        self.records = self.load_records()

    def load_records(self):  # Load patient records from CSV file into a dictionary
        records = {}
        try:
            with open(self.filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pid = row['Patient_ID']
                    if pid not in records:
                        records[pid] = []
                    records[pid].append(row)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"Cannot find patient data file: {self.filepath}")
            print("Patient data file not found.")
        return records

    def save_to_file(self):  # Save current records back to the CSV file
        if not self.records:
            return
        fieldnames = list(next(iter(self.records.values()))[0].keys())
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for visits in self.records.values():
                writer.writerows(visits)

    def get_patient_info(self, pid):  # Return the most recent visit info for a given patient
        if pid in self.records:
            visits = sorted(self.records[pid], key=lambda x: x["Visit_time"], reverse=True)
            return "\n".join([f"{key}: {value}" for key, value in visits[0].items()])
        return None

    def add_patient_record(self, visit_data):  # Add a new visit to an existing or new patient
        pid = visit_data["Patient_ID"]
        if pid in self.records:
            self.records[pid].append(visit_data)
        else:
            self.records[pid] = [visit_data]

    def remove_patient_record(self, pid):  # Remove all visits for a patient
        if pid in self.records:
            del self.records[pid]
            return True
        return False

    def prompt_new_patient_info(self, pid):  # Prompt user to enter patient visit details via simpledialog
        def ask(field, prompt):
            value = simpledialog.askstring(field, prompt)
            if value is None:
                return None
            return value.strip()

        visit_department = ask("Department", "Department visited:")  # Prompt for each required field; cancel if any are skipped
        if visit_department is None: return None

        gender = ask("Gender", "Gender:")
        if gender is None: return None

        race = ask("Race", "Race:")
        if race is None: return None

        age = ask("Age", "Age:")
        if age is None: return None

        ethnicity = ask("Ethnicity", "Ethnicity:")
        if ethnicity is None: return None

        insurance = ask("Insurance", "Insurance:")
        if insurance is None: return None

        zip_code = ask("Zip", "Zip Code:")
        if zip_code is None: return None

        chief_complaint = ask("Complaint", "Chief Complaint:")
        if chief_complaint is None: return None

        note_type = ask("Note Type", "Note Type:")
        if note_type is None: return None

        visit = {   # Create visit entry with generated IDs and current date
            "Patient_ID": pid,
            "Visit_ID": str(random.randint(100000, 999999)),
            "Visit_time": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Visit_department": visit_department,
            "Gender": gender,
            "Race": race,
            "Age": age,
            "Ethnicity": ethnicity,
            "Insurance": insurance,
            "Zip_code": zip_code,
            "Chief_complaint": chief_complaint,
            "Note_ID": str(random.randint(10000000, 99999999)),
            "Note_type": note_type
        }

        return visit
