from books import Record
from books.address_book.error import ContactNotFound, ContactAlreadyExist

def handle_contact_command(command: str, address_book):
    try:
        if command.startswith("add contact "):
            name = command[len("add contact "):].strip()
            record = Record(name)
            address_book.add_record(record)
            print(f"✅ Контакт '{name}' додано.")

        elif command.startswith("show contact "):
            name = command[len("show contact "):].strip()
            record = address_book.find(name)
            print(record)

        elif command.startswith("delete contact "):
            name = command[len("delete contact "):].strip()
            address_book.delete_record(name)
            print(f"🗑️ Контакт '{name}' видалено.")

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
                        print(f"  - {rec.name}")

        elif command.startswith("search contact "):
            keyword = command[len("search contact "):].strip()
            results = address_book.search(keyword)
            if not results:
                print(f"📭 Контактів з ключовим словом '{keyword}' не знайдено.")
            else:
                for rec in results:
                    print(rec)

        else:
            print("⚠️ Команда для контактів не розпізнана.")

    except (ContactNotFound, ContactAlreadyExist) as e:
        print(f"⚠️ {e}")
    except Exception as e:
        print(f"❌ Виникла помилка: {e}")