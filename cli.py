"""
cli.py — Головний CLI-інтерфейс персонального помічника.

Цей модуль забезпечує навігацію між адресною книгою та нотатками,
обробляє введення користувача та викликає відповідні обробники команд.
"""

from colorama import init, Fore, Style
from books import AddressBook, NoteBook
from contact_commands import handle_contact_command
from note_commands import handle_note_command
from cli.guess_command.guess_command import handle_command_with_guess
from cli.guess_command.possible_commands import CONTACT_COMMANDS, NOTE_COMMANDS, GENERAL_COMMANDS

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

def create_general_command_handler(current_mode):
    def handle_general_command(cmd):
        cmd_lower = cmd.lower()
        if cmd_lower in ("exit", "close"):
            return "exit"
        elif cmd_lower == "switch":
            return "notes" if current_mode == "contacts" else "contacts"
        elif cmd_lower == "help":
            print_help()
    return handle_general_command

def run_mode(mode_name, prompt, valid_commands, handler, book):
    general_handler = create_general_command_handler(mode_name)
    try:
        while True:
            command = input(prompt).strip()
            result = handle_command_with_guess(
                command, valid_commands + GENERAL_COMMANDS, handler, book, general_command_callback=general_handler
            )
            if result == "exit":
                return "exit"
            elif result in ("contacts", "notes"):
                return result
    except KeyboardInterrupt:
        print("\n" + Fore.GREEN + "👋 До побачення!")
        exit(0)


def main():
    """
    Точка входу до застосунку. Ініціалізує об'єкти AddressBook і NoteBook,
    надає користувачу можливість перемикатися між режимами
    (контакти / нотатки), вводити команди та отримувати результат.

    Головний цикл програми завершується при введенні 'exit' або 'close'.
    """
    address_book = AddressBook()
    note_book = NoteBook()

    print(Fore.GREEN + "\n👋 Вітаємо у Персональному помічнику!")

    active_mode = None

    while True:
        if active_mode is None:
            print_main_menu()
            section = input(
                Fore.BLUE + "Оберіть розділ (0-3): "
            ).strip()

            if section == "0":
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
            next_mode = run_mode(
                "contacts",
                Fore.BLUE + "[Контакти] >>> ",
                CONTACT_COMMANDS,
                handle_contact_command,
                address_book,
            )
            if next_mode == "exit":
                break
            active_mode = next_mode

        elif active_mode == "notes":
            next_mode = run_mode(
                "notes",
                Fore.YELLOW + "[Нотатки] >>> ",
                NOTE_COMMANDS,
                handle_note_command,
                note_book,
            )
            if next_mode == "exit":
                break
            active_mode = next_mode

if __name__ == "__main__":
    main()