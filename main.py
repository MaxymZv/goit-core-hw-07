from collections import UserDict
from datetime import datetime

#Making class Field that will be used as a base class for Name and Phone
class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass

#Making class Phone 
class Phone(Field):
    def __init__(self, value):
        value = str(value)
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self,value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%D-%M-%Y').date()
            except ValueError:
                raise ValueError("Birthday must be in the format 'DD-MM-YYYY'.")
# Making class Record that will hold contact information
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(None)

    def __str__(self):
        return f'Contact name: {self.name.value}, Phones: {",".join(str(p) for p in self.phones)}'
    
#Method for adding phone number    
    def add_phone(self, phone):
        if isinstance(phone, str):
            phone = Phone(phone)
        self.phones.append(phone)

#Method for removing phone number
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found in record.")

#Method for editing phone number
    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                if isinstance(new_phone, str):   
                    self.phones[index] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found in record.") 

#Method for finding phone number 
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        else:
            return None

#Making class Adressbook that inherits from UserDict    
class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record
    
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def find(self, name):
        return self.data.get(name, None)
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
    





