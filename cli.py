"""
cli.py — Головний CLI-інтерфейс персонального помічника.

Цей модуль забезпечує навігацію між адресною книгою та нотатками,
обробляє введення користувача та викликає відповідні обробники команд.
"""

from colorama import init, Fore, Style
from books import AddressBook, NoteBook
from contact_commands import handle_contact_command
from note_commands import handle_note_command
from storage import save_data, load_data

# Ініціалізація кольорового виводу для CLI
init(autoreset=True)


def print_main_menu():
    """
    Виводить головне меню програми з доступними режимами:
    1 — адресна книга, 2 — нотатки, 3 — допомога, 0 — вихід.
    Також інформує про додаткові команди 'switch', 'help' та 'exit'.
    """
    print(Fore.CYAN + '''
=== ГОЛОВНЕ МЕНЮ ===
1. Адресна книга
2. Нотатки
3. Допомога
0. Вихід

Під час роботи в обраному розділі можна ввести команду:
  switch    - щоб перейти до іншого розділу
  help      - щоб побачити доступні команди
  exit/close - щоб завершити роботу
''')


def print_help():
    """
    Виводить список усіх доступних CLI-команд для роботи
    з контактами, нотатками та навігації в інтерфейсі.
    """
    print(Fore.YELLOW + '''
=== ДОСТУПНІ КОМАНДИ ===

[АДРЕСНА КНИГА]
  add contact <name>
  edit contact <name>
  show contact <name>
  delete contact <name>
  show all contacts
  show birthdays <days>
  search contact <keyword>

[НОТАТКИ]
  add note "<title>" "<text>"
  edit note <title>
  edit tag <title>
  delete tag <title> <tag>
  delete note <title>
  search note <title>
  show all notes
  sort notes by tag

[ЗАГАЛЬНІ]
  switch               - перейти між режимами
  help                 - показати команди
  exit / close         - вихід
''')


def main():
    """
    Точка входу до застосунку. Ініціалізує об'єкти AddressBook і NoteBook,
    надає користувачу можливість перемикатися між режимами
    (контакти / нотатки), вводити команди та отримувати результат.

    Головний цикл програми завершується при введенні 'exit' або 'close'.
    """
    # address_book = AddressBook()
    # note_book = NoteBook()
    address_book, note_book = load_data()

    print(Fore.GREEN + "\n👋 Вітаємо у Персональному помічнику!")

    active_mode = None

    while True:
        if active_mode is None:
            print_main_menu()
            section = input(
                Fore.BLUE + "Оберіть розділ (0-3): "
            ).strip()

            if section == "0":
                save_data(address_book, note_book)
                print(Fore.GREEN + "👋 До побачення!")
                break

            elif section == "1":
                active_mode = "contacts"

            elif section == "2":
                active_mode = "notes"

            elif section == "3" or section.lower() == "help":
                print_help()

            else:
                print(Fore.RED + "⚠️ Невідома опція. Спробуйте ще раз.")

        elif active_mode == "contacts":
            command = input(Fore.BLUE + "[Контакти] >>> ").strip()

            if command.lower() in ("exit", "close"):
                save_data(address_book, note_book)
                print(Fore.GREEN + "👋 До побачення!")
                break

            elif command.lower() == "switch":
                active_mode = "notes"
                continue

            elif command.lower() == "help":
                print_help()
                continue

            handle_contact_command(command, address_book)

        elif active_mode == "notes":
            command = input(Fore.YELLOW + "[Нотатки] >>> ").strip()

            if command.lower() in ("exit", "close"):
                save_data(address_book, note_book)
                print(Fore.GREEN + "👋 До побачення!")
                break

            elif command.lower() == "switch":
                active_mode = "contacts"
                continue

            elif command.lower() == "help":
                print_help()
                continue

            handle_note_command(command, note_book)


if __name__ == "__main__":
    main()