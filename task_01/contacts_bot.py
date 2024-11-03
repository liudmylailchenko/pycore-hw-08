from functools import wraps
from address_book import AddressBook, Record
from address_book_serializer import load_data, save_data


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)

    return inner


@input_error
def add_contact(args, contacts: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Enter the name and phone please.")

    name, phone, *_ = args
    record = contacts.find(name)
    message = f"Contact {name} updated."
    if record is None:
        record = Record(name)
        contacts.add_record(record)
        message = f"Contact {name} added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], contacts: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Enter the name, old phone and new phone please.")

    name, phone_old, phone_new, *_ = args
    record = contacts.find(name)
    if record is None:
        return f"Contact {name} not found."

    record.edit_phone(phone_old, phone_new)
    return f"Contact {name} updated."


@input_error
def show_phone(args: list[str], contacts: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Enter the name please.")

    name = args[0]
    record = contacts.find(name)
    if record is None:
        return f"Contact {name} not found."
    return record.show_all_phones()


@input_error
def show_all(contacts: AddressBook) -> str:
    if not contacts:
        return "No contacts found"
    return contacts


@input_error
def show_upcoming_birthdays(contacts: AddressBook) -> str:
    return contacts.get_upcoming_birthdays()


@input_error
def add_birthday(args: list[str], contacts: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Enter the name and birthday please.")

    name, birthday, *_ = args
    record = contacts.find(name)
    if record is None:
        return f"Contact {name} not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], contacts: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Enter the name please.")

    name = args[0]
    record = contacts.find(name)
    if record is None:
        return f"Contact {name} not found."
    return record.birthday


def main() -> None:
    contacts = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(show_upcoming_birthdays(contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

    save_data(contacts)


if __name__ == "__main__":
    main()
