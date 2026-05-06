"""
delete_data.py

Deletes all files and folders inside the Data directory,
except for data_science_salaries.csv which is preserved.
"""

from Helper.helper import delete_data

if __name__ == "__main__":
    confirm = input("This will delete everything in 'Data' except 'data_science_salaries.csv'. Proceed? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        delete_data()
    else:
        print("Aborted.")
