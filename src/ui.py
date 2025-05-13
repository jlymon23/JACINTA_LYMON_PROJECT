import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import csv
import random
from user import validate_user
from patient import PatientManager
from note import NoteManager
from stats import count_visits_by_date, generate_statistics
from logger import log_action

class ClinicalApp:
    def __init__(self):  # Initialize the main app window and managers
        self.root = tk.Tk()
        self.root.title("Clinical Data Warehouse")
        self.username = None
        self.role = None
        self.patient_mgr = PatientManager("./data/Patient_data.csv")
        self.note_mgr = NoteManager("./data/Notes.csv", "./data/Patient_data.csv")

    def run(self):  # Start the login window
        self.show_login()
        self.root.mainloop()

    def show_login(self):  # Display login form
        self.clear_window()

        tk.Label(self.root, text="Username").grid(row=0, column=0)
        username_entry = tk.Entry(self.root)
        username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password").grid(row=1, column=0)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(row=1, column=1)

        def attempt_login():  # Handle login attempt
            username = username_entry.get()
            password = password_entry.get()
            role = validate_user(username, password)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if role:
                self.username = username
                self.role = role
                log_action(username, role, "LOGIN", timestamp)
                self.show_menu()
            else:
                log_action(username, "unknown", "FAILED_LOGIN", timestamp)
                messagebox.showerror("Login Failed", "Invalid credentials.")

        tk.Button(self.root, text="Log In", command=attempt_login).grid(row=2, column=0, columnspan=2)

    def show_menu(self):  # Display main menu based on user role
        self.clear_window()

        tk.Label(self.root, text=f"Welcome {self.username} ({self.role})").pack()

        if self.role in ["clinician", "nurse"]:
            actions = [
                ("Retrieve Patient", self.retrieve_patient),
                ("Add Patient", self.add_patient),
                ("Remove Patient", self.remove_patient),
                ("Count Visits", self.count_visits),
                ("View Note", self.view_note),
                ("Exit", self.root.quit)
            ]
        elif self.role == "admin":
            actions = [("Count Visits", self.count_visits), ("Exit", self.root.quit)]
        elif self.role == "management":
            actions = [("Generate Key Statistics", self.generate_stats), ("Exit", self.root.quit)]
        else:
            actions = [("Exit", self.root.quit)]

        for (label, command) in actions:
            tk.Button(self.root, text=label, command=command).pack(pady=5)

    def retrieve_patient(self):  # Handle retrieving patient info
        pid = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        result = self.patient_mgr.get_patient_info(pid)
        log_action(self.username, self.role, "RETRIEVE_PATIENT", datetime.datetime.now())
        if result:
            messagebox.showinfo("Patient Info", result)
        else:
            messagebox.showwarning("Not Found", "Patient ID not found.")

    def add_patient(self):  # Handle adding a new patient or visit
        pid = simpledialog.askstring("Add Patient", "Enter Patient ID:")
        data = self.patient_mgr.prompt_new_patient_info(pid)
        if data:
            self.patient_mgr.add_patient_record(data)
            self.patient_mgr.save_to_file()
            log_action(self.username, self.role, "ADD_PATIENT", datetime.datetime.now())
            messagebox.showinfo("Success", "Patient added successfully.")

    def remove_patient(self):  # Handle removing a patient
        pid = simpledialog.askstring("Remove Patient", "Enter Patient ID:")
        if self.patient_mgr.remove_patient_record(pid):
            self.patient_mgr.save_to_file()
            log_action(self.username, self.role, "REMOVE_PATIENT", datetime.datetime.now())
            messagebox.showinfo("Success", "Patient removed.")
        else:
            messagebox.showwarning("Not Found", "Patient ID not found.")

    def count_visits(self):  # Count visits on a specific date
        input_date = simpledialog.askstring("Count Visits", "Enter Date (YYYY-MM-DD):")

        try:
            dt = datetime.datetime.strptime(input_date.strip(), "%Y-%m-%d")
            converted_date = f"{dt.month}/{dt.day}/{dt.year}"
        except ValueError:
            messagebox.showerror("Invalid Format", "Please enter date in YYYY-MM-DD format.")
            return

        count = 0
        for visits in self.patient_mgr.records.values():
            for visit in visits:
                visit_date = visit['Visit_time'].strip()
                if visit_date == converted_date or visit_date == input_date.strip():
                    count += 1

        log_action(self.username, self.role, "COUNT_VISITS", datetime.datetime.now())
        messagebox.showinfo("Visit Count", f"Total visits on {input_date}: {count}")

    def view_note(self):  # View clinical note for a patient by visit date
        pid = simpledialog.askstring("View Note", "Enter Patient ID:")
        visit_date = simpledialog.askstring("View Note", "Enter Visit Date (YYYY-MM-DD):")
        note = self.note_mgr.get_note_by_patient_and_date(pid, visit_date)
        log_action(self.username, self.role, "VIEW_NOTE", datetime.datetime.now())
        if note:
            messagebox.showinfo("Note Content", note)
        else:
            messagebox.showwarning("Not Found", "No note found for this patient on that date.")

    def generate_stats(self):  # Generate and save statistical plots
        generate_statistics(self.patient_mgr.records)
        log_action(self.username, self.role, "GENERATE_STATS", datetime.datetime.now())
        messagebox.showinfo("Done", "Statistics saved to output folder.")

    def clear_window(self):  # Clear all current UI elements
        for widget in self.root.winfo_children():
            widget.destroy()
