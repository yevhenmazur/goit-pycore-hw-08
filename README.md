# goit-pycore-hw-08

Topic 12: Homework. Serializing and copying objects in Python

## Description
Console bot for saving contacts and birthdays

## Usage
To run the bot use `main.py`

The bot support the following commands:

1. `add [name] [phone]`: Add either a new contact with a name and phone number or a phone number to an existing contact. You can add multiple phone numbers.
2. `change [name] [old phone] [new phone]`: Change the phone number for the specified contact.
3. `phone [name]`: Show the phone numbers for the specified contact.
4. `all`: Show all contacts in the address book.
5. `add-birthday [name] [date of birth]`: Add the date of birth for the specified contact.
6. `show-birthday [name]`: Show the date of birth for the specified contact.
7. `birthdays`: Show the birthdays that are coming up in the next week.
8. `hello`: Send a greeting from the bot.
9. `close` or `exit`: Close the program.

## Example Usage
Here are some example commands and their outputs:

```
Welcome to the assistant bot!
Enter a command >>> hello
How can I help you?

Enter a command >>> add John 1234567890
New contact with name John added. Phone 1234567890 added.

Enter a command >>> phone John
1234567890

Enter a command >>> add-birthday John 1990-05-23
Birthday for John added

Enter a command >>> show-birthday John
1990-05-23

Enter a command >>> birthdays
Name                 Celebration Day
-----------------------------------
John                 2024.05.23     

Enter a command >>> exit
Good bye!
```