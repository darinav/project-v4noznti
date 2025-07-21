from colorama import Fore
from books import AddressBook, Record, address_book_errors

import re

def _find_record_exact(book: AddressBook, name: str):
    try:
        return book.find(name)
    except address_book_errors.ContactNotFound:
        pass
    return None

def _format_record_row(record: Record):
    phones = ', '.join(ph for ph in record.phones)
    emails = ', '.join(em for em in record.emails)
    return [record.name, phones, emails, record.address, str(record.birthday or '')]

def _print_contacts_table(records: list[Record]):
    headers = [
        "Ім'я",
        "Телефон",
        "Email",
        "Адреса",
        "ДН"
    ]
    rows = [_format_record_row(r) for r in records]
    if not rows:
        print(Fore.YELLOW + "Немає контактів для виводу.")
        return

    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + rows))]

    def fmt_row(row_data):
        return " │ ".join(str(cell).ljust(w) for cell, w in zip(row_data, col_widths))

    border = "─┼─".join("─" * w for w in col_widths)

    print(Fore.CYAN + fmt_row(headers))
    print(Fore.MAGENTA + border)
    for row in rows:
        print(fmt_row(row))

def ask_valid_birthday():
    while True:
        birthday = input(Fore.RED + "Введіть день народження (ДД.ММ.РРРР або Enter): ").strip()
        if not birthday:
            return ""
        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", birthday):
            return birthday
        print(Fore.RED + "❌ Формат дати має бути ДД.ММ.РРРР (наприклад, 21.07.2024).")

def _parse_days(parts):
    if len(parts) > 2:
        try:
            days = int(parts[2])
            if days < 1 or days > 365:
                days = 7
        except Exception:
            days = 7
    else:
        days = 7
    return days

def handle_contact_command(command: str, book: AddressBook) -> None:
    parts = command.strip().split()
    if not parts:
        print(Fore.RED + "⚠️ Порожня команда.")
        return

    action = parts[0].lower()

    if action in ("help", "exit", "close", "switch"):
        return

    if action == "add" and len(parts) >= 2 and parts[1] == "contact":
        name = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть ім'я контакта: ").strip()
        if not name:
            print(Fore.RED + "⚠️ Ім'я не може бути порожнім.")
            return
        try:
            record = Record(name)
            phone = input(Fore.YELLOW + "Введіть телефон (або Enter): ").strip()
            if phone:
                record.add_phone(phone)
            email = input(Fore.CYAN + "Введіть email (або Enter): ").strip()
            if email:
                record.add_email(email)
            address = input(Fore.GREEN + "Введіть адресу (або Enter): ").strip()
            if address:
                record.add_address(address)
            birthday = ask_valid_birthday()
            if birthday:
                record.add_birthday(birthday)
            book.add_record(record)
            print(Fore.GREEN + f"✅ Контакт '{name}' додано!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    elif action == "edit" and len(parts) >= 2 and parts[1] == "contact":
        name = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть ім'я контакта для редагування: ").strip()
        if not name:
            print(Fore.RED + "⚠️ Ім'я не може бути порожнім.")
            return
        record = _find_record_exact(book, name)
        if not record:
            print(Fore.RED + f"❌ Контакт з ім'ям '{name}' не знайдено.")
            return
        try:
            phone = input(Fore.YELLOW + "Новий телефон (або Enter): ").strip()
            if phone:
                record.edit_phone('', phone)
            email = input(Fore.CYAN + "Новий email (або Enter): ").strip()
            if email:
                record.edit_email('', email)
            address = input(Fore.GREEN + "Нова адреса (або Enter): ").strip()
            if address:
                record.edit_address(address)
            birthday = ask_valid_birthday()
            if birthday:
                record.edit_birthday(birthday)
            print(Fore.GREEN + f"✅ Контакт '{name}' оновлено!")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    elif action == "delete" and len(parts) >= 2 and parts[1] == "contact":
        name = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть ім'я контакта для видалення: ").strip()
        if not name:
            print(Fore.RED + "⚠️ Ім'я не може бути порожнім.")
            return
        record = _find_record_exact(book, name)
        if not record:
            print(Fore.RED + f"❌ Контакт з ім'ям '{name}' не знайдено.")
            return
        try:
            book.delete_record(name)
            print(Fore.GREEN + f"🗑️ Контакт '{name}' видалено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    elif action == "show" and len(parts) >= 2 and parts[1] == "contact":
        name = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть ім'я контакта для перегляду: ").strip()
        if not name:
            print(Fore.RED + "⚠️ Ім'я не може бути порожнім.")
            return
        record = _find_record_exact(book, name)
        if not record:
            print(Fore.RED + f"❌ Контакт з ім'ям '{name}' не знайдено.")
            return
        _print_contacts_table([record])

    elif command == "show all contacts":
        records: list[Record] = [r for _, r in book.items()]
        if records:
            _print_contacts_table(records)
        else:
            print(Fore.YELLOW + "Адресна книга порожня.")

    elif parts[0] == "show" and parts[1] == "birthdays":
        days = _parse_days(parts)
        records: list[Record] = [
            r for r, _ in sorted(book.upcoming_birthdays(upcoming_birthdays_period=days), key=lambda i: i[1])
        ]
        if records:
            print(Fore.CYAN + f"Контакти, у яких день народження у наступні {days} днів:")
            _print_contacts_table(records)
        else:
            print(Fore.YELLOW + "Немає контактів із днями народження у цей період.")

    elif parts[0] == "search" and parts[1] == "contact":
        keyword = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть фразу для пошуку: ").strip()
        if not keyword:
            print(Fore.RED + "⚠️ Пошуковий запит не може бути порожнім.")
            return
        records: list[Record] = book.search(keyword)
        if records:
            _print_contacts_table(records)
        else:
            print(Fore.YELLOW + "Контактів не знайдено.")

    else:
        print(Fore.RED + "⚠️ Невідома команда для контактів.")
