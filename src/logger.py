# logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "./output/usage_log.csv" # Define the path to the log file where usage data will be recorded

def log_action(username, role, action, timestamp=None):
    if not timestamp:  # Use current timestamp if one isn't supplied
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("output", exist_ok=True) # Ensure the output directory exists

    log_exists = os.path.exists(LOG_FILE)  # Check if the log file already exists
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:  # Open the log file in append mode
        writer = csv.writer(f)
        if not log_exists:  # If this is a new file, write the header first
            writer.writerow(["Username", "Role", "Action", "Timestamp"])
        writer.writerow([username, role, action, timestamp])  # Write the actual log entry
