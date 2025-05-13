# stats.py
import matplotlib.pyplot as plt
import pandas as pd
import os

def count_visits_by_date(records, date):  # Count the number of visits on a specific date
    count = 0
    for visits in records.values():
        for visit in visits:
            if visit['Visit_time'] == date:
                count += 1
    return count

def generate_statistics(records):  # Generate bar, pie, and histogram plots from patient data
    # Flatten records into a list of visits
    visits = []
    for patient_visits in records.values():
        visits.extend(patient_visits)

    df = pd.DataFrame(visits)

    os.makedirs("output", exist_ok=True)  # Ensure output folder exists

    # Plot 1: Number of visits by department
    dept_counts = df['Visit_department'].value_counts()
    dept_counts.plot(kind='bar', title='Visits by Department')
    plt.xlabel("Department")
    plt.ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("output/visits_by_department.png")
    plt.clf()

    # Plot 2: Gender distribution
    gender_counts = df['Gender'].value_counts()
    gender_counts.plot(kind='pie', title='Gender Distribution', autopct='%1.1f%%')
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("output/gender_distribution.png")
    plt.clf()

    # Plot 3: Age distribution
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Age'].dropna().astype(int).hist(bins=10)
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.savefig("output/age_distribution.png")
    plt.clf()
