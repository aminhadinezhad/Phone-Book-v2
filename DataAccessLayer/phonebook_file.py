"""Reading and writing contacts in the CSV file."""
import csv
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # Running as PhoneBook.exe: keep the file next to the exe,
    # not in the temporary folder PyInstaller unpacks the program into.
    _APP_FOLDER = Path(sys.executable).resolve().parent
else:
    # Running as a .py file: keep it next to main.py,
    # no matter which folder the program is started from.
    _APP_FOLDER = Path(__file__).resolve().parent.parent

FILE_PATH = _APP_FOLDER / "PhoneBook.csv"

FIELDS = ["First Name", "Last Name", "Phone Number", "Mobile Number1", "Mobile Number2", "Address", "Postal Code"]

# utf-8-sig lets Excel show Persian text correctly.
_ENCODING = "utf-8-sig"


def load_contacts():
    """Return all saved contacts as a list of dicts keyed by FIELDS."""
    if not FILE_PATH.exists():
        return []
    with open(FILE_PATH, newline="", encoding=_ENCODING) as file:
        return [{field: row.get(field) or "" for field in FIELDS} for row in csv.DictReader(file)]


def save_contact(contact):
    """Add one contact to the end of the file, keeping the ones already there."""
    is_new_file = not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0
    with open(FILE_PATH, mode="a", newline="", encoding=_ENCODING) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(contact)


def save_all_contacts(contacts):
    """Replace the whole file with the given contacts (used after deleting)."""
    with open(FILE_PATH, mode="w", newline="", encoding=_ENCODING) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(contacts)
