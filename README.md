# Phone-Book

A simple command-line phone book written in Python. Contacts are stored in `PhoneBook.csv`.

This is the improved second version. The original first version is kept at
[aminhadinezhad/Phone-Book](https://github.com/aminhadinezhad/Phone-Book).

## Features

- Add, list, search and delete contacts from a menu
- Every field is validated before saving, and the program asks again until the value is valid
- Accepts Persian names and Persian/Arabic digits (`۰۹۱۲...` is saved as `0912...`)
- Spaces and dashes in numbers are ignored (`0912-345-6789` → `09123456789`)
- The CSV file opens correctly in Excel, including Persian text

## Validation rules

| Field | Required | Rule |
|---|---|---|
| First Name / Last Name | yes | letters (English or Persian) and spaces |
| Phone Number | yes | 8 digits not starting with `0`, or 11 digits starting with `0` |
| Mobile Number1 | yes | 11 digits starting with `09` |
| Mobile Number2 | no | same as Mobile Number1 |
| Address | no | anything |
| Postal Code | no | 10 digits |

## Project structure

```
main.py                            menu and user interaction
BusinessLogicLayer/validation.py   rules for checking and cleaning input
DataAccessLayer/phonebook_file.py  reading and writing PhoneBook.csv
```

## Run

Requires Python 3.8 or newer. No extra packages are needed.

```
python main.py
```

## Build a Windows .exe

```
python -m pip install pyinstaller
python -m PyInstaller --onefile --name PhoneBook --noconfirm main.py
```

The program is created at `dist\PhoneBook.exe` and runs without installing Python.
`PhoneBook.csv` is saved next to the exe.
