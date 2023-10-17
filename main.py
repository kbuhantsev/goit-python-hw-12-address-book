from address_book import AddressBook, Record
from random import randrange

CLOSE_COMMANDS = ("good bye", "close", "exit")


def input_error(function):
    def wrapper(*args):
        try:
            result = function(*args)
        except KeyError as ke:
            return str(ke)
        except ValueError as ve:
            return str(ve)
        except TypeError:
            return "Missing required parameters!"
        return result

    return wrapper


@input_error
def hello() -> str:
    return "How can I help you?"


@input_error
def add(name: str, phone_number: str) -> str:
    record = Record(name)
    record.add_phone(phone_number)
    book.add_record(record)
    return "added: name-{} phone-{}".format(name, phone_number)


@input_error
def change(name: str, phone_number: str, new_phone_number) -> str:
    record = book.find(name)
    if record is None:
        raise KeyError("Can not find contact!")
    record.edit_phone(phone_number, new_phone_number)
    return "changed: name-{} phone-{}".format(name, phone_number)


@input_error
def phone(name: str) -> str:
    record = book.find(name)
    if record is None:
        raise KeyError("Can not find contact!")
    return str(record)


@input_error
def show_all() -> str:
    result = ""
    for part in book:
        part = "".join(f"{value} \n" for value in part.values())
        result += part
    return result


@input_error
def find_global(part: str) -> str:
    result_list = book.global_search(part)
    if len(result_list) == 0:
        return "nothing were found..."
    return "".join(f"{record} \n" for record in result_list)


def help_func() -> str:
    return (' hello - to greeting you\n \
add {name} {phone} - adds new contact\n \
change {name} {phone} - changes existing contact\n \
phone {name} - returns phone number\n \
find - finding contacts by part of given string \n \
show_all - shows all contacts\n \
generate - generates 20 test contacts\n \
good bye, close, exit - to exit')


def generate() -> str:
    for i in range(1, 21):
        record = Record(
            name="test_" + str(i),
            birthday=f"{str(randrange(1970, 2023))}.{str(randrange(1, 12))}.{str(randrange(1, 30))}")
        record.add_phone(str(randrange(1000000000, 9999999999)))
        book.add_record(record)
    return "success"


OPERATIONS = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "find": find_global,
    "show_all": show_all,
    "help": help_func,
    "generate": generate,
}


def input_parser(text):
    sub_string = text.split()
    if len(sub_string) == 1:
        return sub_string[0], None
    return sub_string[0], *sub_string[1:]


if __name__ == "__main__":

    book = AddressBook()

    print("You can use 'help' command to see all commands")

    while True:

        input_text = input(">>> ").lower().strip()
        if input_text in CLOSE_COMMANDS:
            print("Good bye!")
            break

        command, *other_args = input_parser(input_text)

        func = OPERATIONS.get(command, None)
        if not func:
            print("Wrong command")
            continue

        if not all(other_args):
            print(func())
        else:
            print(func(*other_args))

        book.save_to_file()
