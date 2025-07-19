"""
contact_commands.py — модуль для обробки команд контактів у CLI-застосунку.

Забезпечує логіку додавання, редагування, перегляду, пошуку та видалення
контактів у адресній книзі, а також перегляд майбутніх днів народження.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colorama import Fore
from books import AddressBook, Record
from books.address_book.error import (
    ContactNotFound,
    ContactAlreadyExist,
    ContactPhoneAlreadyExist,
    ContactEmailAlreadyExist,
    ContactAddressAlreadyExist,
    ContactBirthdayAlreadyExist,
)

def handle_contact_command(command: str, book: AddressBook) -> None:
    """
    Обробляє CLI-команду для роботи з контактами.

    Аргументи:
        command (str): текст команди, введений користувачем.
        book (AddressBook): об'єкт адресної книги.

    Підтримувані команди:
        - add contact <name>
        - edit contact <name>
        - delete contact <name>
        - show contact <name>
        - show all contacts
        - show birthdays <days>
        - search contact <keyword>
    """
    parts = command.strip().split()
    if not parts:
        print(Fore.RED + "⚠️ Порожня команда.")
        return

    action = parts[0].lower()

    # Додавання нового контакту
    if action == "add" and len(parts) >= 3 and parts[1] == "contact":
        """
        Додає новий контакт із введеним ім’ям, телефоном, email,
        адресою та днем народження.
        """
        name = " ".join(parts[2:])
        try:
            record = Record(name)
            print(Fore.YELLOW + "Введіть телефон (або Enter): ", end="")
            phone = input().strip()
            if phone:
                record.add_phone(phone)

            print(Fore.CYAN + "Введіть email (або Enter): ", end="")
            email = input().strip()
            if email:
                record.add_email(email)

            print(Fore.GREEN + "Введіть адресу (або Enter): ", end="")
            address = input().strip()
            if address:
                record.add_address(address)

            print(Fore.RED + "Введіть день народження (DD.MM.YYYY): ", end="")
            birthday = input().strip()
            if birthday:
                record.add_birthday(birthday)

            book.add_record(record)
            print(Fore.GREEN + f"✅ Контакт '{name}' додано!")

        except ContactAlreadyExist:
            print(Fore.RED + f"❌ Контакт '{name}' вже існує!")
        except ContactPhoneAlreadyExist:
            print(Fore.RED + f"❌ Телефон '{phone}' вже існує у цьому контакті!")
        except ContactEmailAlreadyExist:
            print(Fore.RED + f"❌ Email '{email}' вже існує у цьому контакті!")
        except ContactAddressAlreadyExist:
            print(Fore.RED + f"❌ Адреса '{address}' вже існує у цьому контакті!")
        except ContactBirthdayAlreadyExist:
            print(Fore.RED + f"❌ День народження вже встановлено для цього контакту!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Редагування існуючого контакту
    elif action == "edit" and len(parts) >= 3 and parts[1] == "contact":
        """
        Редагує перший телефон, email, адресу та день народження обраного контакту.
        """
        name = " ".join(parts[2:])
        try:
            record = book.find(name)
            print(Fore.YELLOW + "Новий телефон (або Enter): ", end="")
            phone = input().strip()
            if phone:
                if record.phones:
                    # Edit existing phone
                    old_phone = record.phones[0]
                    record.edit_phone(old_phone, phone)
                else:
                    # Add new phone if none exists
                    record.add_phone(phone)

            print(Fore.CYAN + "Новий email (або Enter): ", end="")
            email = input().strip()
            if email:
                if record.emails:
                    # Edit existing email
                    old_email = record.emails[0]
                    record.edit_email(old_email, email)
                else:
                    # Add new email if none exists
                    record.add_email(email)

            print(Fore.GREEN + "Нова адреса (або Enter): ", end="")
            address = input().strip()
            if address:
                record.edit_address(address)

            print(Fore.RED + "Новий день народження (або Enter): ", end="")
            birthday = input().strip()
            if birthday:
                record.edit_birthday(birthday)

            print(Fore.GREEN + f"✅ Контакт '{name}' оновлено!")
        except ContactNotFound:
            print(Fore.RED + f"❌ Контакт '{name}' не знайдено!")
        except ContactPhoneAlreadyExist:
            print(Fore.RED + f"❌ Телефон '{phone}' вже існує у цьому контакті!")
        except ContactEmailAlreadyExist:
            print(Fore.RED + f"❌ Email '{email}' вже існує у цьому контакті!")
        except ContactAddressAlreadyExist:
            print(Fore.RED + f"❌ Адреса '{address}' вже існує у цьому контакті!")
        except ContactBirthdayAlreadyExist:
            print(Fore.RED + f"❌ День народження вже встановлено для цього контакту!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Видалення контакту
    elif action == "delete" and len(parts) >= 3 and parts[1] == "contact":
        """
        Видаляє контакт за іменем.
        """
        name = " ".join(parts[2:])
        try:
            book.delete_record(name)
            print(Fore.GREEN + f"🗑️ Контакт '{name}' видалено.")
        except ContactNotFound:
            print(Fore.RED + f"❌ Контакт '{name}' не знайдено!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Показ одного контакту
    elif action == "show" and len(parts) >= 3 and parts[1] == "contact":
        """
        Виводить повну інформацію про контакт за ім’ям.
        """
        name = " ".join(parts[2:])
        try:
            print(book.find(name))
        except ContactNotFound:
            print(Fore.RED + f"❌ Контакт '{name}' не знайдено!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Показ усіх контактів
    elif command == "show all contacts":
        """
        Виводить усі контакти з адресної книги.
        """
        for record in book:
            print(record)

    # Показ майбутніх днів народження
    elif parts[0] == "show" and parts[1] == "birthdays":
        """
        Показує список контактів, у яких день народження
        настане протягом вказаної кількості днів.
        """
        try:
            days = int(parts[2]) if len(parts) > 2 else 7
            records = book.upcoming_birthdays_by_days(days)
            for r in records:
                print(r)
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Пошук контактів
    elif parts[0] == "search" and parts[1] == "contact":
        """
        Пошук контактів за ключовим словом у імені, телефоні, email тощо.
        """
        keyword = " ".join(parts[2:])
        results = book.search(keyword)
        for r in results:
            print(r)

    # Невідома команда
    else:
        """
        Виводить повідомлення про помилку у випадку невідомої команди.
        """
        print(Fore.RED + "⚠️ Невідома команда для контактів.")