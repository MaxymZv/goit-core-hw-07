from collections import UserDict
from datetime import datetime
from functools import wraps



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
                value = datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                raise ValueError("Birthday must be in the format 'DD.MM.YYYY'.")
        super().__init__(value)
        
# Making class Record that will hold contact information
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f'Contact name: {self.name.value}, Phones: {",".join(str(p) for p in self.phones)}'
    
    def add_birthday(self, birthday):
        if isinstance(birthday, str):
            birthday = Birthday(birthday)
        self.birthday = birthday
    
    def get_birthday(self):
        if self.birthday:
            return self.birthday.value
        return None

    
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
    
    def get_upcoming_birthday(self):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday and isinstance(record.birthday, Birthday):
                birthday_date = record.birthday.value
                if birthday_date.month == today.month and birthday_date.day >= today.day:
                    upcoming_birthdays.append((record.name.value, birthday_date))
        return upcoming_birthdays
    

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())



def parse_input(user_input):                           
    cmd, *args = user_input.split()                      
    cmd = cmd.lower().strip()                            
    return cmd, *args                                    


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs) 
        except IndexError:                             
            return 'Please give me name and phone number!'
        except KeyError:                               
            return 'Ther is no such person in contacts!'
        except ValueError:                             
            return 'Give me name and phone number please'
    return inner
    

@input_error
def add_contacts(args, book):
    name, phone, *_ = args
    record = book.find(name)
    massage = 'Contact updated'
    if record is None:
        record = Record(name)
        book.add_record(record)
    if phone:
        record.add_phone(phone)
    return massage

@input_error
def change_contacts(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f'No contact found with name {name}')
    record.edit_phone(new_phone)
    return f'Phone number for {name} changed from {old_phone} to {new_phone}'

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f'No contact found with name {name}')
    phones = ', '.join(str(phone) for phone in record.phones)
    return f'Phone numbers for {name}: {phones}' if phones else f'No phone numbers found for {name}'

def show_all_contacts(book):
    if not book.data:
        return 'No contacts found.'
    return '\n'.join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError(f'No contact found with name {name}')
    record.add_birthday(birthday)
    return f'Birthday for {name} added: {record.birthday.value}' if record.birthday else f'No birthday found for {name}'

@input_error
def show_birthdays(args ,book):
    person_birthday = record.get_birthday()
    if not record.get_birthday():
        return 'No upcoming birthdays found.'
    return '\n'.join(f'{name}: {date}' for name, date in person_birthday)

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthday()
    if not upcoming_birthdays:
        return 'No upcoming birthdays found.'
    if record is None:
        raise KeyError(f'No contact found with name {name}')
    elif book.get_upcoming_birthday():
        return f'Birthday for {name}: {book.get_upcoming_birthday()}'
    


    


def main():
    book = AddressBook()                                       
    print('Welcome to assistant bot!')                   
    while True:                                         
        user_input = input('Enter command: ')
        command, *args = parse_input(user_input)

        if command in ['exit', 'close']:
            print('Goodbye!')
            break                                        
        elif command == 'hello':
            print('How can i help you?')
        elif command == 'add':          
            print(add_contacts(args, book))
        elif command == 'all':
            print(f'All contacts: {show_all_contacts(book)}')
        elif command == 'change':
            print(change_contacts(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthdays':
            print(show_birthdays(args, book))
        elif command == 'birthdays':
            print(birthdays(book))
        else:                                             
            print('Invalid command!') 


if __name__ == '__main__':
    main()  





