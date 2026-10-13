from BusinessLogicLayer.validation import (
    is_valid_mobile_number,
    is_valid_name,
    is_valid_phone_number,
    is_valid_postal_code,
    normalize_name,
    normalize_number,
)
from DataAccessLayer.phonebook_file import FIELDS, load_contacts, save_all_contacts, save_contact

NAME_ERROR = "Please enter a valid name (letters and spaces only)."
PHONE_ERROR = "Please enter a valid Phone Number (8 digits, or 11 digits starting with '0')."
MOBILE_ERROR = "Please enter a valid Mobile Number (11 digits starting with '09')."
POSTAL_ERROR = "Please enter a valid Postal Code (10 digits)."


def ask(prompt, is_valid, error_message, normalize=str.strip, required=True):
    """Keep asking until the user types a valid value, then return it.

    If required is False, an empty answer is accepted and returned as "".
    """
    while True:
        value = normalize(input(prompt))
        if value == "" and not required:
            return ""
        if is_valid(value):
            return value
        print(error_message)


def ask_yes_no(prompt):
    """Return True for yes/y and False for no/n; ask again for anything else."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please answer 'yes' or 'no'.")


def print_contacts(contacts):
    """Print contacts numbered from 1, skipping empty fields."""
    for number, contact in enumerate(contacts, start=1):
        print(f"\n{number}. {contact['First Name']} {contact['Last Name']}")
        for field in FIELDS[2:]:
            if contact[field]:
                print(f"   {field}: {contact[field]}")


def add_contacts():
    while True:
        print("\nFields marked with * are required.")
        contact = {
            "First Name": ask("First Name*: ", is_valid_name, NAME_ERROR, normalize_name),
            "Last Name": ask("Last Name*: ", is_valid_name, NAME_ERROR, normalize_name),
            "Phone Number": ask("Phone Number*: ", is_valid_phone_number, PHONE_ERROR, normalize_number),
            "Mobile Number1": ask("Mobile Number1*: ", is_valid_mobile_number, MOBILE_ERROR, normalize_number),
            "Mobile Number2": ask("Mobile Number2: ", is_valid_mobile_number, MOBILE_ERROR, normalize_number, required=False),
            "Address": input("Address: ").strip(),
            "Postal Code": ask("Postal Code: ", is_valid_postal_code, POSTAL_ERROR, normalize_number, required=False),
        }
        save_contact(contact)
        print("Contact saved successfully.")

        if not ask_yes_no("Do you want to add another contact? (yes/no): "):
            return


def show_all_contacts():
    contacts = load_contacts()
    if not contacts:
        print("\nThe phone book is empty.")
        return
    print_contacts(contacts)
    print(f"\nTotal: {len(contacts)} contact(s).")


def search_contacts():
    term = input("\nSearch for a name or number: ").strip().lower()
    if term == "":
        return
    number_term = normalize_number(term)

    found = []
    for contact in load_contacts():
        text = " ".join(contact.values()).lower()
        if term in text or (number_term and number_term in text):
            found.append(contact)

    if not found:
        print("No contact found.")
        return
    print_contacts(found)


def delete_contact():
    contacts = load_contacts()
    if not contacts:
        print("\nThe phone book is empty.")
        return
    print_contacts(contacts)

    choice = normalize_number(input("\nNumber of the contact to delete (Enter to cancel): "))
    if choice == "":
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(contacts):
        print("There is no contact with that number.")
        return

    index = int(choice) - 1
    full_name = f"{contacts[index]['First Name']} {contacts[index]['Last Name']}"
    if ask_yes_no(f"Delete {full_name}? (yes/no): "):
        contacts.pop(index)
        save_all_contacts(contacts)
        print(f"{full_name} was deleted.")


def main():
    actions = {
        "1": add_contacts,
        "2": show_all_contacts,
        "3": search_contacts,
        "4": delete_contact,
    }
    while True:
        print("\n===== Phone Book =====")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search")
        print("4. Delete contact")
        print("5. Exit")
        choice = normalize_number(input("Choose an option: "))

        if choice == "5":
            print("Goodbye!")
            return
        if choice in actions:
            actions[choice]()
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or a closed input: exit quietly instead of showing an error.
        print("\nGoodbye!")
