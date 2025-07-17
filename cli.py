from books import AddressBook, NoteBook
from contact_commands import handle_contact_command
from note_commands import handle_note_command

def print_main_menu():
    print("""
=== ГОЛОВНЕ МЕНЮ ===
1. Адресна книга
2. Нотатки
3. Допомога
0. Вихід
""")

def print_help():
    print("""
=== ДОСТУПНІ КОМАНДИ ===

[АДРЕСНА КНИГА]
  add contact <name>
  show contact <name>
  delete contact <name>
  show all contacts
  show birthdays <days>
  search contact <keyword>

[НОТАТКИ]
  add note "<title>" "<text>"
  search note <title>
  delete note <title>
  show all notes
  sort notes by tag
""")

def main():
    address_book = AddressBook()
    note_book = NoteBook()

    print("\n👋 Вітаємо у Персональному помічнику!")

    while True:
        print_main_menu()
        section = input("Оберіть розділ (0-3): ").strip()

        if section == "0":
            print("👋 До побачення!")
            break

        elif section == "1":  # Address Book
            while True:
                command = input("[Контакти] >>> ").strip()
                if command.lower() in ("back", "exit", "close"):
                    break
                handle_contact_command(command, address_book)

        elif section == "2":  # Notes
            while True:
                command = input("[Нотатки] >>> ").strip()
                if command.lower() in ("back", "exit", "close"):
                    break
                handle_note_command(command, note_book)

        elif section == "3" or section.lower() == "help":
            print_help()

        else:
            print("⚠️ Невідома опція. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
