'''Module Main is a main entry-point'''
import pickle
from actions import AddressBook, Record, NoneRecordFound, InvalidPhoneNumberFormat, DateValueError

def input_error(func):
    '''The decorator to process erros in user input'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DateValueError:
            return "Please check the date format. It should be YYYY.MM.DD"
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me the name"
        except KeyError:
            return "Ask about one of your contact, or use 'all' command"
        except InvalidPhoneNumberFormat:
            return "Please check the phone number. It should be 10 digits"
        except NoneRecordFound:
            return "Please check the contact name or use 'all' command"

    return inner

def parse_input(user_input):
    '''The function to parse user input'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    '''Process command "add" with str arguments "name" and "Phone number"'''
    name, phone, *_ = args
    try:
        record = book.find(name)
    except NoneRecordFound:
        record = Record(name)
        book.add_record(record)
        message = f"New contact with name {record.name} added."
    else:
        message = f"Contact with name {record.name.value} updated."
    if phone:
        record.add_phone(phone)
        message = message + f" Phone {record.phones[-1]} added."
    book.add_record(record)
    return message

@input_error
def change_contact(args, book):
    '''Process command "change" with str arguments "name" and "Phone number"'''
    name, oldphone, newphone, *_ = args
    record = book.find(name)
    record.edit_phone(oldphone, newphone)
    return "Contact changed"

@input_error
def return_phone(args, book):
    '''Process command "phone" with str argument "name"'''
    name, *_ = args
    record = book.find(name)
    message = ", ".join(str(phone) for phone in record.phones)
    return message

@input_error
def add_birthday(args, book):
    '''Add birthday to the record'''
    name, birthday, *_ = args
    record = book.find(name)
    if record.birthday is None:
        record.add_birthday(birthday)
        return f"Birthday for {record.name} added"
    else:
        record.add_birthday(birthday)
        return f"Birthday for {record.name} updated"

@input_error
def show_birthday(args, book):
    '''Show birthday for specific record'''
    name, *_ = args
    record = book.find(name)
    return record.birthday

@input_error
def birthdays(book):
    '''Show all upcomming birthdays'''
    upcoming_birthdays_list = book.get_upcoming_birthdays()
    return upcoming_birthdays_list

def save_data(book, filename="addressbook.pkl"):
    '''The function to serialize the addressbook'''
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    '''The function to deserialize the addressbook'''
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    '''Main function to control the bot'''
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command >>> ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(return_phone(args, book))
        elif command == "all":
            if not book.data:
                print("No contacts found")
            else:
                for name, record in book.data.items():
                    print(record)
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            birthday_list = birthdays(book)
            if not birthday_list:
                message = "No upcoming birthdays within the next 7 days."
                print(message)
                continue

            print(f"{'Name':<20} {'Celebration Day':<15}")
            print("-" * 35)
            for birthday in birthday_list:
                name = birthday["name"]
                celebration_day = birthday["celebration_day"]
                print(f"{name:<20} {celebration_day:<15}")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
