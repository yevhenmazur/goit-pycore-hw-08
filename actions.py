'''The actions module contains a description of the main classes and methods'''
import re
from collections import UserDict
from datetime import datetime, timedelta

class InvalidPhoneNumberFormat(Exception):
    '''Raised when input phone number is not 10 digits'''

class NoneRecordFound(Exception):
    '''Raised when none record found'''

class DateValueError(ValueError):
    '''Raised when input date in incorrect format'''

class Field:
    '''Basic class for text information'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    '''The class for contact name'''

class Phone(Field):
    '''The class for phone number'''

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        '''Isolate the value for Phone'''
        return self._value

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 10:
            self._value = new_value
        else:
            raise InvalidPhoneNumberFormat("Phone number must be a string of 10 digits.")

class Birthday(Field):
    '''The class for phone number'''
    def __init__(self, value: str):
        try:
            date_value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise DateValueError() from Birthday
        super().__init__(date_value)

    def __str__(self):
        return self.value.strftime("%Y-%m-%d")

    def __repr__(self):
        return self.value.strftime("%Y-%m-%d")

class Record:
    '''This class contain objects of Class Name and list of objects from class Phone'''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        '''
        The method add the phone number in to list, and check
        if the phone number has correct format
        '''
        if bool(re.match(r'^\d{10}$', phone)):
            self.phones.append(Phone(phone))
        else:
            raise InvalidPhoneNumberFormat

    def add_birthday(self, birthday: Birthday):
        '''This method allow to add a birthday to contact'''
        self.birthday = Birthday(birthday)

    def edit_phone(self, old_phone: str, new_phone: str):
        '''This method allow to replace the old_phone with the new_phone'''
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index].value = new_phone

    def remove_phone(self, phone_to_remove: str):
        '''This method allow to remove the phone number'''
        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_remove:
                del self.phones[index]

    # def find_phone(self, phone_to_search: str) -> Phone:
    #     '''This method accept phone number and return existing Phone object'''
    #     for index, phone in enumerate(self.phones):
    #         if phone.value == phone_to_search:
    #             return phone.value
    #     return None

    def find_phone(self, phone_to_search: str) -> Phone:
        '''This method accepts a phone number and returns the existing Phone object'''
        for phone in self.phones:
            if phone.value == phone_to_search:
                return phone
        return None


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    '''The main class for object for user interract with'''

    def add_record(self, record):
        '''
        Method to add object Record in to AddressBook
        The Record will be associated with key value record.name
        '''
        self.data[record.name] = record

    def find(self, name_to_search: str) -> Record:
        '''This method performs search of the Record type object by his name'''
        for name, record in self.data.items():
            if name.value == name_to_search:
                return record
        raise NoneRecordFound

    def delete(self, name_to_delete: str) -> None:
        '''This method delete existing Record object from the AddressBook'''
        record_to_delete = self.find(name_to_delete)
        key_to_delete = record_to_delete.name
        del self.data[key_to_delete]

    def get_upcoming_birthdays(self) -> list:
        """
        The function calculates birthdays based on the employee's date of birth
        and assigns a date for congratulations within 7 days to one of the working days of the week.
        """
        current_date = datetime.today().date()
        current_year = current_date.year
        upcoming_birthdays = list()
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday = record.birthday.value
            birthday_this_year = (birthday.replace(year = current_year)).date()
            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(year = current_year + 1)
            days_to_birthday = birthday_this_year - current_date
            if days_to_birthday <= timedelta(days=7):
                if birthday_this_year.weekday() == 5: # Saturday
                    celebration_day = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6: # Sunday
                    celebration_day = birthday_this_year + timedelta(days=1)
                else:
                    celebration_day = birthday_this_year
                celebration_day = celebration_day.strftime("%Y.%m.%d")
                upcoming_birthdays.append({
                    "name": record.name.value, 
                    "celebration_day": celebration_day
                })
        return upcoming_birthdays
