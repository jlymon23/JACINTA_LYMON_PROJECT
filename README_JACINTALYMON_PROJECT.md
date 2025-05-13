# Clinical Data Warehouse System

This is a Python-based GUI application for managing patient data, clinical notes, and usage statistics. The system supports multiple user roles with varying access levels and was built for a final project in a healthcare informatics course.

## How to Run the Program

To run the program from terminal or command prompt, navigate to the project directory and run:

```bash
python main.py
```

This will launch the graphical interface. Ensure all CSV files are located in the `data/` folder.

## Requirements

To install the necessary packages, use:

```bash
pip install -r requirements.txt
```

This project uses the following packages:
- matplotlib

Note: `tkinter` is a standard library in Python and does not need separate installation.

## Project Structure

```
JACINTA_LYMON_PROJECT/
├── data/               # Input data (CSV files)
│   ├── Patient_data.csv
│   ├── Notes.csv
│   └── Credentials.csv
├── output/             # Output logs and charts
│   └── logs.txt
├── src/                # Source code
│   ├── ui.py
│   ├── patient.py
│   ├── note.py
│   ├── stats.py
│   ├── user.py
│   └── logger.py
├── UML.png             # UML Class Diagram
├── main.py             # Main entry point
├── requirements.txt    # Required packages
└── README.md           # Documentation
```

## Features

- Add new patients and visits
- Remove patient records
- Retrieve most recent patient visit info
- Count visits by specific date
- View clinical notes by patient and date
- Generate statistics for management (visual charts)
- Log all user actions and login attempts

## Roles and Permissions

| Role        | Access |
|-------------|--------|
| clinician   | Full access to patients and notes |
| nurse       | Full access to patients and notes |
| admin       | Can count visits |
| management  | Can generate key statistics |

## Notes for Users and Developers

- Do not modify the structure of the provided CSV files. The column headers are essential for program functionality.
- The log file (`logs.txt`) will be generated in the `output/` directory.
- Ensure Python 3.7 or later is installed.

Author: Jacinta Lymon  
Course: HI 741 – Spring 2025 Final Project
