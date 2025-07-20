from colorama import Fore, Style
from books import AddressBook, Record

import re
import datetime

def _find_record_exact(book: AddressBook, name: str):
    try:
        record = book.find(name)
        if record and getattr(record, "name", None) == name:
            return record
    except Exception:
        pass
    return None

def _format_record_row(record, birthday_override=None):
    phones = ', '.join(str(ph) for ph in getattr(record, 'phones', []) if ph)
    emails = ', '.join(str(em) for em in getattr(record, 'emails', []) if em)
    address = getattr(record, 'address', '')
    birthday = (birthday_override if birthday_override else getattr(record, 'birthday', '')) or ''
    if hasattr(birthday, 'value'):
        birthday = birthday.value
    return [
        str(getattr(record, 'name', '')),
        phones,
        emails,
        address,
        birthday
    ]

def _print_contacts_table(records):
    headers = [
        "Ім'я",
        "Телефон",
        "Email",
        "Адреса",
        "ДН"
    ]
    rows = []
    for r in records:
        if isinstance(r, tuple) and len(r) == 2 and hasattr(r[0], "name"):
            rows.append(_format_record_row(r[0], birthday_override=r[1]))
        else:
            rows.append(_format_record_row(r))
    if not rows:
        print(Fore.YELLOW + "Немає контактів для виводу.")
        return

    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + rows))]
    def fmt_row(row):
        return " │ ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))

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

def _filter_birthdays(records, days):
    today = datetime.date.today()
    upcoming = []
    for r in records:
        b = getattr(r, 'birthday', None)
        date_value = None
        if hasattr(b, 'value'):
            b = b.value
        if isinstance(b, str) and re.match(r"\d{2}\.\d{2}\.\d{4}", b):
            try:
                day, month, year = map(int, b.split('.'))
                date_value = datetime.date(today.year, month, day)
                if date_value < today:
                    date_value = datetime.date(today.year + 1, month, day)
            except Exception:
                continue
        elif isinstance(b, datetime.date):
            date_value = b.replace(year=today.year)
            if date_value < today:
                date_value = date_value.replace(year=today.year + 1)
        if date_value:
            delta = (date_value - today).days
            if 0 <= delta <= days:
                upcoming.append((r, date_value.strftime('%d.%m.%Y')))
    return upcoming

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
        records = list(book.values()) if hasattr(book, 'values') else list(book)
        if records:
            _print_contacts_table(records)
        else:
            print(Fore.YELLOW + "Адресна книга порожня.")

    elif parts[0] == "show" and parts[1] == "birthdays":
        days = _parse_days(parts)
        records = list(book.values()) if hasattr(book, 'values') else list(book)
        output_rows = _filter_birthdays(records, days)
        if output_rows:
            print(Fore.CYAN + f"Контакти, у яких день народження у наступні {days} днів:")
            _print_contacts_table(output_rows)
        else:
            print(Fore.YELLOW + "Немає контактів із днями народження у цей період.")

    elif parts[0] == "search" and parts[1] == "contact":
        keyword = " ".join(parts[2:]) if len(parts) > 2 else input(Fore.CYAN + "Введіть фразу для пошуку: ").strip()
        if not keyword:
            print(Fore.RED + "⚠️ Пошуковий запит не може бути порожнім.")
            return
        results = list(book.search(keyword))
        if results:
            _print_contacts_table(results)
        else:
            print(Fore.YELLOW + "Контактів не знайдено.")

    else:
        print(Fore.RED + "⚠️ Невідома команда для контактів.")
