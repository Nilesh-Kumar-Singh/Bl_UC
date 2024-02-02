'''
@Author: Nilesh Kumar SIngh
@Date: 02-02-2024
@Last Modified by: Nilesh Kumar Singh
@Last Modified time: 02-02-2024
@Title : exception handling
'''
import csv
import json
import sys
import logging

logging.basicConfig(filename = 'address_book.log', level = logging.INFO, format = '%(asctime)s:%(name)s:%(message)s')
logger = logging.getLogger()

class EmptyInputError(Exception):
    pass

class Contact:
    def __init__(self, contact_data):
        self.first_name = contact_data["first_name"]
        self.last_name = contact_data["last_name"]
        self.address = contact_data["address"]
        self.city = contact_data["city"]
        self.state = contact_data["state"]
        self.zip_code = contact_data["zip_code"]
        self.phone_number = contact_data["phone_number"]
        self.email = contact_data["email"]

    def __str__(self):
        return f"First Name: {self.first_name}\nLast Name: {self.last_name}\nAddress: {self.address}\nCity: {self.city}\nState: {self.state}\nZip Code: {self.zip_code}\nPhone Number: {self.phone_number}\nEmail: {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class AddressBook:
    def __init__(self, name, system):
        self.name = name
        self.system = system
        self.collection = Collection()
        self.contacts = []

    def add_contact(self, new_contact):
        try:
            if not all(new_contact.__dict__.values()):
                raise ValueError("Contact data cannot be empty.")

            if not self.is_duplicate(new_contact.first_name, new_contact.last_name):
                self.contacts.append(new_contact)
                print("Contact Added Successfully!")
                logger.info(f"Contact added to address book '{self.name}': {new_contact}")
                self.collection.store(self.name, new_contact)
            else:
                print("Contact already exists in the address book.")
                logger.warning(f"Attempt to add duplicate contact to address book '{self.name}': {new_contact}")
        except ValueError as ve:
            print(f"Error: {ve}")
            logger.error(f"Error adding contact to address book '{self.name}': {ve}")

    def is_duplicate(self, first_name, last_name):
        for contact in self.contacts:
            if contact.first_name == first_name and contact.last_name == last_name:
                return True
        return False

    def display_contacts(self):
        if self.name in self.collection.books:
            sorted_contacts = sorted(self.contacts, key=lambda contact: contact.get_full_name())
            for contact in sorted_contacts:
                print("\n" + "-"*20 + "\n")
                print(f"\u2192 {self.name} \u2190\n")
                print(contact)
                print("\n" + "-"*20 + "\n")
        else:
            print(f"Address book '{self.name}' not found.")
            logger.warning(f"Attempt to display contacts from non-existent address book '{self.name}'")

    def sort_contacts_by_city(self):
        sorted_contacts = sorted(self.contacts, key=lambda contact: contact.city)
        self.display_sorted_contacts(sorted_contacts, "City")

    def sort_contacts_by_state(self):
        sorted_contacts = sorted(self.contacts, key=lambda contact: contact.state)
        self.display_sorted_contacts(sorted_contacts, "State")

    def sort_contacts_by_zip(self):
        sorted_contacts = sorted(self.contacts, key=lambda contact: contact.zip_code)
        self.display_sorted_contacts(sorted_contacts, "Zip Code")

    def display_sorted_contacts(self, sorted_contacts, sort_criteria):
        if self.name in self.collection.books:
            print(f"Sorted contacts in Address Book '{self.name}' by {sort_criteria}:")
            for contact in sorted_contacts:
                print("\n" + "-"*20 + "\n")
                print(f"\u2192 {self.name} \u2190\n")
                print(contact)
                print("\n" + "-"*20 + "\n")
        else:
            print(f"Address book '{self.name}' not found.")
            logger.warning(f"Attempt to display sorted contacts from non-existent address book '{self.name}'")


    def edit_contact(self, first_name):
        for contact in self.contacts:
            if contact.first_name == first_name:
                print("1. Last Name")
                print("2. Address")
                print("3. City")
                print("4. State")
                print("5. Zip Code")
                print("6. Phone Number")
                print("7. Email")
                options = input("Which Detail You want to Edit: ")
                if options == '1':
                    contact.last_name = input("Last Name: ")
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '2':
                    contact.address = input("Address: ")
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '3':
                    old_city = contact.city
                    contact.city = input("City: ")
                    self.system.update_city_person_map(old_city, contact, self.name)
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '4':
                    old_state = contact.state
                    contact.state = input("State: ")
                    self.system.update_state_person_map(old_state, contact, self.name)
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '5':
                    contact.zip_code = input("Zip Code: ")
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '6':
                    contact.phone_number = input("Phone Number: ")
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                elif options == '7':
                    contact.email = input("Email: ")
                    print("Contact Updated Successfully!")
                    logger.info(f"Contact updated in address book '{self.name}': {contact}")
                else:
                    print("Invalid Input")
                    logger.warning(f"Invalid edit option selected for contact in address book '{self.name}'")
                return f"First Name: {contact.first_name}\nLast Name: {contact.last_name}\nAddress: {contact.address}\nCity: {contact.city}\nState: {contact.state}\nZip Code: {contact.zip_code}\nPhone Number: {contact.phone_number}\nEmail: {contact.email}"
        print(f"Contact with first name '{first_name}' not found.")
        logger.warning(f"Attempt to edit non-existent contact in address book '{self.name}': {first_name}")

    def delete_contact(self, first_name):
        for contact in self.contacts:
            if contact.first_name == first_name:
                self.contacts.remove(contact)
                print("Contact deleted successfully!")
                logger.info(f"Contact deleted from address book '{self.name}': {contact}")
                return
        print(f"Contact with first name '{first_name}' not found.")
        logger.warning(f"Attempt to delete non-existent contact from address book '{self.name}': {first_name}")


class AddressBookSystem:
    def __init__(self):
        self.address_books = {}
        self.city_person_map = {}
        self.state_person_map = {}

    def add_address_book(self, name):
        try:
            if not name.strip():
                raise EmptyInputError("Address book name cannot be empty or whitespace.")

            if name not in self.address_books:
                self.address_books[name] = AddressBook(name, self)
                print(f"Address book '{name}' added successfully!")
                logger.info(f"Address book added: {name}")
            else:
                print(f"Address book with name '{name}' already exists.")
                logger.warning(f"Attempt to add duplicate address book: {name}")
        except EmptyInputError as e:
            print(f"Error: {e}")
            logger.error(f"Error adding address book: {e}")

    def delete_address_book(self, name):
        if name in self.address_books:
            del self.address_books[name]
            print(f"Address book '{name}' deleted successfully!")
            logger.info(f"Address book deleted: {name}")
        else:
            print(f"Address book '{name}' not found.")
            logger.warning(f"Attempt to delete non-existent address book: {name}")

    def get_address_book(self, name):
        if name in self.address_books:
            return self.address_books[name]
        else:
            print(f"Address book '{name}' not found.")
            return None

    def display_address_books(self):
        print("List of Address Books:")
        for name in self.address_books:
            print(f"- {name}")

    def add_person_to_city_map(self, contact):
        city = contact.city.lower()  # Convert city to lowercase
        if city in self.city_person_map.keys():
            self.city_person_map[city].append((self.get_address_book_name(contact), contact))
        else:
            self.city_person_map[city] = [(self.get_address_book_name(contact), contact)]

    def update_city_person_map(self, old_city, contact, address_book_name):
        old_city = old_city.lower()  # Convert city to lowercase
        new_city = contact.city.lower()  # Convert city to lowercase
        if old_city in self.city_person_map:
            self.city_person_map[old_city] = [(name, contact) for name, contact in self.city_person_map[old_city] if name != address_book_name]
            if new_city in self.city_person_map:
                self.city_person_map[new_city].append((address_book_name, contact))
            else:
                self.city_person_map[new_city] = [(address_book_name, contact)]
        else:
            print(f"City '{old_city}' not found in city_person_map.")

    def add_person_to_state_map(self, contact):
        state = contact.state.lower()  # Convert state to lowercase
        if state in self.state_person_map:
            self.state_person_map[state].append((self.get_address_book_name(contact), contact))
        else:
            self.state_person_map[state] = [(self.get_address_book_name(contact), contact)]

    def update_state_person_map(self, old_state, contact, address_book_name):
        old_state = old_state.lower()  # Convert state to lowercase
        new_state = contact.state.lower()  # Convert state to lowercase
        if old_state in self.state_person_map:
            self.state_person_map[old_state] = [(name, contact) for name, contact in self.state_person_map[old_state] if name != address_book_name]
            if new_state in self.state_person_map:
                self.state_person_map[new_state].append((address_book_name, contact))
            else:
                self.state_person_map[new_state] = [(address_book_name, contact)]
        else:
            print(f"State '{old_state}' not found in state_person_map.")
        
    def get_address_book_name(self, contact):
        for name, address_book in self.address_books.items():
            if contact in address_book.contacts:
                return name
        return None

    def search_person(self, query, search_type):
        query = query.lower()  # Convert query to lowercase
        if search_type == "city":
            results = self.city_person_map.get(query, [])  # Search with lowercase query
        elif search_type == "state":
            results = self.state_person_map.get(query, [])  # Search with lowercase query
        else:
            print("Invalid search type.")
            return

        return results

    def count_persons_by_city(self):
        city_counts = {}
        for city, persons in self.city_person_map.items():
            city_counts[city] = len(persons)
        return city_counts

    def count_persons_by_state(self):
        state_counts = {}
        for state, persons in self.state_person_map.items():
            state_counts[state] = len(persons)
        return state_counts

    def save_address_book_to_csv(self, name, file_path):
        if not file_path.endswith('.csv'):
            print("Error: File path must end with '.csv'.")
            return

        address_book = self.get_address_book(name)
        if address_book:
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["first_name", "last_name", "address", "city", "state", "zip_code", "phone_number", "email"])
                writer.writeheader()
                for contact in address_book.contacts:
                    writer.writerow(vars(contact))
            print(f"Address book '{name}' saved to CSV file '{file_path}' successfully!")
        else:
            print(f"Address book '{name}' not found.")

    def load_address_book_from_csv(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            address_book_name = file_path.split('.')[0]  # Use file name as address book name
            address_book = AddressBook(address_book_name)
            for row in reader:
                contact_data = {
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "address": row["address"],
                    "city": row["city"],
                    "state": row["state"],
                    "zip_code": row["zip_code"],
                    "phone_number": row["phone_number"],
                    "email": row["email"]
                }
                new_contact = Contact(contact_data)
                address_book.add_contact(new_contact)
                self.add_person_to_city_map(new_contact)
                self.add_person_to_state_map(new_contact)
            self.address_books[address_book_name] = address_book
        print(f"Address book loaded from CSV file '{file_path}' successfully!")

    def save_address_book_to_json(self, name, file_path):
        if not file_path.endswith('.json'):
            print("Error: File path must end with '.json'.")
            return

        address_book = self.get_address_book(name)
        if address_book:
            with open(file_path, 'w') as file:
                json.dump([vars(contact) for contact in address_book.contacts], file, indent=4)
            print(f"Address book '{name}' saved to JSON file '{file_path}' successfully!")
        else:
            print(f"Address book '{name}' not found.")

    def load_address_book_from_json(self, file_path):
        with open(file_path, 'r') as file:
            contacts_data = json.load(file)
            address_book_name = file_path.split('.')[0]  # Use file name as address book name
            address_book = AddressBook(address_book_name)
            for contact_data in contacts_data:
                new_contact = Contact(contact_data)
                address_book.add_contact(new_contact)
                self.add_person_to_city_map(new_contact)
                self.add_person_to_state_map(new_contact)
            self.address_books[address_book_name] = address_book
        print(f"Address book loaded from JSON file '{file_path}' successfully!")

def menu(address_book_system):
    while True:
        print(f"\u2192 Menu \u2190")
        print("1. Add Address Book")
        print("2. Delete Address Book")
        print("3. Add Contact")
        print("4. Display Contacts")
        print("5. Edit Contact")
        print("6. Delete Contact")
        print("7. Search Person by City or State")
        print("8. Display Address Books")
        print("9. Get Count of Contact Persons by City or State")
        print("10. Sort Contacts by City")
        print("11. Sort Contacts by State")
        print("12. Sort Contacts by Zip Code")
        print("13. Save Address Book to CSV")
        print("14. Load Address Book from CSV")
        print("15. Save Address Book to JSON")
        print("16. Load Address Book from JSON")
        print("17. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                name = get_non_empty_input("Enter the name of the new Address Book: ")
                address_book_system.add_address_book(name)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                name = get_non_empty_input("Enter the name of the Address Book to delete: ")
                address_book_system.delete_address_book(name)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    first_name = get_non_empty_input("Enter First Name: ")
                    last_name = get_non_empty_input("Enter Last Name: ")
                    address = get_non_empty_input("Enter Address: ")
                    city = get_non_empty_input("Enter City: ")
                    state = get_non_empty_input("Enter State: ")
                    zip_code = get_non_empty_input("Enter Zip Code: ")
                    phone_number = get_non_empty_input("Enter Phone Number: ")
                    email = get_non_empty_input("Enter Email: ")

                    contact_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "address": address,
                        "city": city,
                        "state": state,
                        "zip_code": zip_code,
                        "phone_number": phone_number,
                        "email": email
                    }

                    new_contact = Contact(contact_data)
                    address_book.add_contact(new_contact)
                    address_book_system.add_person_to_city_map(new_contact)
                    address_book_system.add_person_to_state_map(new_contact)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '4':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    address_book.display_contacts()
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '5':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    first_name = get_non_empty_input("Enter the first name of the contact you want to edit: ")
                    updated_contact = address_book.edit_contact(first_name)
                    print("Updated Contact:")
                    print(updated_contact)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '6':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    first_name = get_non_empty_input("Enter the first name of the contact you want to delete: ")
                    address_book.delete_contact(first_name)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '7':
            try:
                search_type = input("Enter 'city' or 'state' to search: ")
                if search_type not in ["city", "state"]:
                    print("Invalid search type.")
                    continue
                query = get_non_empty_input(f"Enter {search_type} to search: ")
                results = address_book_system.search_person(query, search_type)
                if results:
                    print("Search Results:")
                    for address_book_name, contact in results:
                        print(f"From Address Book '{address_book_name}':")
                        print(contact)
                else:
                    print("No matching contacts found.")
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '8':
            address_book_system.display_address_books()
        elif choice == '9':
            try:
                search_type = input("Enter 'city' or 'state' to get count: ")
                if search_type not in ["city", "state"]:
                    print("Invalid search type.")
                    continue
                if search_type == "city":
                    counts = address_book_system.count_persons_by_city()
                elif search_type == "state":
                    counts = address_book_system.count_persons_by_state()
                print(f"Counts by {search_type.capitalize()}:")
                for location, count in counts.items():
                    print(f"{location}: {count}")
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '10':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    address_book.sort_contacts_by_city()
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '11':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    address_book.sort_contacts_by_state()
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '12':
            try:
                name = get_non_empty_input("Enter the name of the Address Book: ")
                address_book = address_book_system.get_address_book(name)
                if address_book:
                    address_book.sort_contacts_by_zip()
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '13':
            try:
                name = get_non_empty_input("Enter the name of the Address Book to save: ")
                file_path = get_non_empty_input("Enter the file path to save CSV: ")
                address_book_system.save_address_book_to_csv(name, file_path)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '14':
            try:
                file_path = get_non_empty_input("Enter the file path to load CSV: ")
                address_book_system.load_address_book_from_csv(file_path)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '15':
            try:
                name = get_non_empty_input("Enter the name of the Address Book to save: ")
                file_path = get_non_empty_input("Enter the file path to save JSON: ")
                address_book_system.save_address_book_to_json(name, file_path)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '16':
            try:
                file_path = get_non_empty_input("Enter the file path to load JSON: ")
                address_book_system.load_address_book_from_json(file_path)
            except EmptyInputError as e:
                print(f"Error: {e}")
        elif choice == '17':
            sys.exit()
        else:
            print("Invalid choice!")

def get_non_empty_input(prompt):
    user_input = input(prompt)
    if not user_input.strip():
        raise EmptyInputError("Input cannot be empty or whitespace.")
    return user_input

class Collection:
    def __init__(self):
        self.books = {}

    def store(self, book_name, book_obj):
        if book_name in self.books:
            self.books[book_name].append(book_obj)
        else:
            self.books[book_name] = [book_obj]

if __name__ == "__main__":
    address_book_system = AddressBookSystem()
    menu(address_book_system)
