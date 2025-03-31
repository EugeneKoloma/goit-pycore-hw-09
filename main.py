from collections import UserDict
import re
from colorama import Fore

class WrongPhoneNumber(Exception):
    def __init__(self, message="Wrong number."):
        self.message = f"{Fore.RED}[ERR]{Fore.RESET}" + message + " Example: +380112223344"
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    __phone_pattern = re.compile(r"^\+?3?8?(0\d{9})$|^0\d{9}$")

    @staticmethod
    def __validate_phone_number(phone_number):
        return bool(Phone.__phone_pattern.match(phone_number))
    
    def __init__(self, phone: str):
        if not Phone.__validate_phone_number(phone):
            raise WrongPhoneNumber(f"Wrong phone number {phone} during adding.")
        super().__init__(phone)

    @property
    def phone(self):
        return self.value

    @phone.setter
    def phone(self, new_phone):
        if not Phone.__validate_phone_number(new_phone):
            raise WrongPhoneNumber(f"Wrong phone number {new_phone} during editing.")
        self.value = new_phone

class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        try:
            self.phones.append(Phone(phone))
        except WrongPhoneNumber as error:
            print(error)
        

    def edit_phone(self, previous_phone, new_phone):
        try:
            found_phone = self.find_phone(previous_phone)
            found_phone.phone = new_phone
        except WrongPhoneNumber as error:
            print(error)

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        self.phones.remove(found_phone)

    def find_phone(self, phone: str):
        found_phone = next((item for item in self.phones if item.value == phone), None)
        return found_phone

    def __str__(self):
        return  f"Contact name: {Fore.CYAN}{self.name.value}{Fore.RESET}, " \
                f"phones: {Fore.YELLOW}{' '.join(p.value for p in self.phones)}{Fore.RESET}"
    
class AdressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data[name]
    
    def delete(self, name):
        self.data.pop(name)

if __name__ == "__main__":
    book = AdressBook()

    john_record = Record("John")
    john_record.add_phone("+380112223344")
    john_record.add_phone("+380115556677")

    jane_record = Record("Jane")
    jane_record.add_phone("+380112223344")
    jane_record.add_phone("+380115556677")

    book.add_record(john_record)
    book.add_record(jane_record)

    book.delete("Jane")

    for name, record in book.data.items():
        print(record)
    
    