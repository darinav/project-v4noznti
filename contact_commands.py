from books import Record
from books.address_book.error import ContactNotFound, ContactAlreadyExist
from colorama import Fore, Style

def handle_contact_command(command: str, address_book):
    try:
        if command.startswith("add contact "):
            name = command[len("add contact "):].strip()
            if name in address_book:
                print(Fore.RED + f"⚠️ Контакт '{name}' вже існує.")
                return

            record = Record(name)
            
            phone = input("📞 Введіть телефон: ").strip()
            if phone:
                record.add_phone(phone)

            email = input("📧 Введіть email: ").strip()
            if email:
                record.add_email(email)

            address = input("🏠 Введіть адресу: ").strip()
            if address:
                record.add_address(address)

            birthday = input("🎂 Введіть дату народження (YYYY-MM-DD): ").strip()
            if birthday:
                record.set_birthday(birthday)

            address_book.add_record(record)
            print(Fore.GREEN + f"✅ Контакт '{name}' успішно додано.")

        elif command.startswith("edit contact "):
            name = command[len("edit contact "):].strip()
            record = address_book.find(name)

            print(f"✏️ Редагування контакту: {Fore.BLUE + name}")
            phone = input("📞 Новий телефон (Enter щоб пропустити): ").strip()
            email = input("📧 Новий email (Enter щоб пропустити): ").strip()
            address = input("🏠 Нова адреса (Enter щоб пропустити): ").strip()
            birthday = input("🎂 Нова дата народження (Enter щоб пропустити): ").strip()

            if phone:
                record.edit_phone(phone)
            if email:
                record.edit_email(email)
            if address:
                record.edit_address(address)
            if birthday:
                record.set_birthday(birthday)

            print(Fore.GREEN + f"✅ Контакт '{name}' оновлено.")

        elif command.startswith("show contact "):
            name = command[len("show contact "):].strip()
            record = address_book.find(name)
            print(record)

        elif command.startswith("delete contact "):
            name = command[len("delete contact "):].strip()
            address_book.delete_record(name)
            print(Fore.YELLOW + f"🗑️ Контакт '{name}' видалено.")

        elif command == "show all contacts":
            if not address_book.data:
                print("📭 Немає контактів.")
            else:
                for record in address_book.values():
                    print(record)

        elif command.startswith("show birthdays"):
            try:
                days = int(command[len("show birthdays"):].strip())
            except ValueError:
                days = 7
            upcoming = address_book.upcoming_birthdays_by_days(days)
            if not upcoming:
                print("📭 Немає днів народжень у найближчі дні.")
            else:
                for date, records in upcoming.items():
                    print(f"\n📅 {date}:")
                    for rec in records:
                        print(f"  - {Fore.BLUE + rec.name}")

        elif command.startswith("search contact "):
            keyword = command[len("search contact "):].strip()
            results = address_book.search(keyword)
            if not results:
                print(f"📭 Контактів з ключовим словом '{keyword}' не знайдено.")
            else:
                for rec in results:
                    print(rec)

        else:
            print(Fore.RED + "⚠️ Команда для контактів не розпізнана.")

    except (ContactNotFound, ContactAlreadyExist) as e:
        print(Fore.RED + f"⚠️ {e}")
    except Exception as e:
        print(Fore.RED + f"❌ Виникла помилка: {e}")
