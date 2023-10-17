from collections import UserDict
from datetime import date
from pathlib import Path
import pickle


class Field:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, contact_name: str):
        super().__init__(self.__validate_name(contact_name))

    @property
    def contact_name(self):
        return self.value

    @contact_name.setter
    def contact_name(self, contact_name: str):
        self.value = self.__validate_name(contact_name)

    @staticmethod
    def __validate_name(contact_name: str) -> str:
        if len(contact_name) < 2:
            raise ValueError("Name must be minimum 2 characters!")
        return contact_name


class Phone(Field):
    def __init__(self, contact_phone: str):
        super().__init__(self.__validate_phone(contact_phone))

    @property
    def contact_phone(self):
        return self.value

    @contact_phone.setter
    def contact_phone(self, contact_phone: str):
        self.value = self.__validate_phone(contact_phone)

    @staticmethod
    def __validate_phone(contact_phone: str) -> str:
        if not len(contact_phone) == 10:
            raise ValueError("Phone number must be 10 digits!")
        elif not contact_phone.isdigit():
            raise ValueError("Phone number must contain only digits!")
        return contact_phone


class Birthday(Field):
    def __init__(self, contact_birthday: str):
        super().__init__(self.__validate_date(contact_birthday))

    @property
    def contact_birthday(self):
        return self.value

    @contact_birthday.setter
    def contact_birthday(self, contact_birthday: str):
        self.value = self.__validate_date(contact_birthday)

    @staticmethod
    def __validate_date(contact_birthday: str) -> None or date:
        if contact_birthday is None:
            return None
        date_array = contact_birthday.split(".")
        try:
            date_value = date(
                int(date_array[0]), int(date_array[1]), int(date_array[2])
            )
            return date_value
        except Exception:
            raise ValueError("birthday must have YYYY.MM.DD format!")


class Record:
    def __init__(self, name: str, birthday: str = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.contact_birthday is not None:
            contact_birthday = self.birthday.contact_birthday
            current_day = date.today()
            birthday = contact_birthday.replace(year=current_day.year)
            if current_day > birthday:
                birthday = contact_birthday.replace(year=current_day.year + 1)
            difference = (birthday - current_day).days
            return difference

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def find_phone(self, phone: str) -> str:
        phones_list = list(filter(lambda p: p.value == phone, self.phones))
        return phones_list[0] if len(phones_list) else None

    def edit_phone(self, phone: str, new_phone: str) -> None:
        for record in self.phones:
            if record.value == phone:
                record.value = new_phone
                return
        raise ValueError("Phone number does not exist!")

    def __str__(self):
        return f"Contact name: {self.name},\
                phones: {'; '.join(p.value for p in self.phones)}, \
                birthday: {self.birthday}"


class AddressBook(UserDict):
    FILE_NAME = "data.bin"

    def __init__(self):
        super().__init__()
        self.__portion_size = 5
        self.data = self.load_from_file

    @property
    def load_from_file(self):
        file = Path.joinpath(Path.cwd(), AddressBook.FILE_NAME)
        if file.exists():
            with open(AddressBook.FILE_NAME, "rb") as fh:
                return pickle.load(fh)
        return {}

    def save_to_file(self):
        with open(AddressBook.FILE_NAME, "wb") as fh:
            pickle.dump(self.data, fh)

    @property
    def portion_size(self):
        return self.__portion_size

    @portion_size.setter
    def portion_size(self, portion_size):
        if portion_size <= 0:
            raise ValueError("Portion size must be 1 or more items!")
        self.__portion_size = portion_size

    def add_record(self, record: Record) -> None:
        self.data.setdefault(record.name.value, record)

    def find(self, name: str):
        if name not in self.data:
            return None
        return self.data[name]

    def global_search(self, string) -> list:
        result = []
        for name, record in self.data.items():
            if name.find(string) != -1:
                result.append(record)
                continue
            for number in record.phones:
                if number.value.find(string) != -1:
                    result.append(record)
                    break
        return result

    def delete(self, name: str) -> None:
        if name in self.data:
            self.data.pop(name)

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state

    def __iter__(self):
        self.current_portion = 0
        return self

    def __next__(self):
        data_list = list(self.data.items())
        _tmp = data_list[
            self.current_portion: self.current_portion + self.portion_size
        ]
        if len(_tmp) == 0:
            raise StopIteration
        else:
            self.current_portion += self.portion_size
            result = {}
            for key, value in _tmp:
                result.setdefault(key, value)
            return result
