import csv
from datetime import datetime

class NoteManager:
    def __init__(self, note_file, patient_file):  # Initialize file paths and load data
        self.note_file = note_file
        self.patient_file = patient_file
        self.notes = self.load_notes()
        self.visits = self.load_patient_visits()

    def load_notes(self):  # Load all clinical notes from CSV into a list of dictionaries
        notes = []
        try:
            with open(self.note_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    notes.append(row)
        except FileNotFoundError:
            print("Note file not found.")
        return notes

    def load_patient_visits(self):  # Load all patient visit records from CSV into a list
        visits = []
        try:
            with open(self.patient_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    visits.append(row)
        except FileNotFoundError:
            print("Patient data file not found.")
        return visits

    def get_note_by_patient_and_date(self, patient_id, visit_date):  # Return a clinical note based on patient ID and visit date
        visit_id = None

        try:    # Convert input date to match format in visit data
            dt = datetime.fromisoformat(visit_date.strip())  
            formatted_input_date = f"{dt.month}/{dt.day}/{dt.year}"
        except ValueError:
            print("[DEBUG] Invalid date format.")
            return None

        print(f"[DEBUG] User entered: Patient ID = '{patient_id}', Visit Date (converted) = '{formatted_input_date}'")

        for visit in self.visits:  # Match patient visit
            visit_pid = visit['Patient_ID'].strip()
            visit_time = visit['Visit_time'].strip()
            print(f"[DEBUG] Checking visit row: Patient_ID = '{visit_pid}', Visit_time = '{visit_time}'")

            if visit_pid == patient_id.strip() and visit_time == formatted_input_date:
                visit_id = visit['Visit_ID']
                print(f"[DEBUG] Found matching visit. Visit_ID = '{visit_id}'")
                break

        if not visit_id:
            print("[DEBUG] No visit found for that patient and date.")
            return None

        print(f"[TEST] Will now search for notes with Patient_ID={patient_id.strip()} and Visit_ID={visit_id.strip()}")

        for note in self.notes:  # Match and return the corresponding note
            note_pid = note['Patient_ID'].strip()
            note_vid = note['Visit_ID'].strip()
            print(f"[DEBUG] Checking note row: Patient_ID = '{note_pid}', Visit_ID = '{note_vid}'")

            if note_pid == patient_id.strip() and note_vid == visit_id.strip():
                print("[DEBUG] Found matching note.")
                return f"Note ID: {note['Note_ID']}\n\n{note['Note_text']}"

        print("[DEBUG] No matching note found for Visit ID.")
        return None
