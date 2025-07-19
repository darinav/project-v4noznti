"""
note_commands.py — модуль для обробки команд нотаток у CLI-застосунку.

Забезпечує додавання, редагування, пошук, сортування, видалення нотаток та тегів
у межах об'єкта NoteBook.
"""

from colorama import Fore
from books import NoteBook, Note
from books.note_book.error import *


def handle_note_command(command: str, notebook: NoteBook):
    """
    Обробляє CLI-команди, пов’язані з нотатками.

    Аргументи:
        command (str): текст введеної команди.
        notebook (NoteBook): об’єкт для зберігання і керування нотатками.

    Підтримувані команди:
        - add note "<title>" "<text>"
        - edit note <title>
        - edit tag <title>
        - delete tag <title> <tag>
        - delete note <title>
        - search note <keyword>
        - show all notes
        - sort notes by tag
    """
    parts = command.strip().split()

    if not parts:
        print(Fore.RED + "⚠️ Порожня команда.")
        return

    action = parts[0].lower()

    # Додавання нової нотатки
    if action == "add" and len(parts) >= 3 and parts[1] == "note":
        # Parse quoted strings properly
        import re
        # Find all quoted strings in the command
        quoted_parts = re.findall(r'"([^"]*)"', command)
        if len(quoted_parts) >= 2:
            title = quoted_parts[0]
            text = quoted_parts[1]
        else:
            # Fallback to original parsing if quotes are not used properly
            title = parts[2].strip('"')
            text = " ".join(parts[3:]).strip('"')

        try:
            note = Note(title, text)
            notebook.add_note(note)
            print(Fore.GREEN + f"✅ Нотатку '{title}' додано.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Редагування тексту нотатки
    elif action == "edit" and len(parts) >= 3 and parts[1] == "note":
        title = parts[2]

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound(title)

            note = notebook.get_note(index)

            print("Новий текст нотатки: ", end="")
            new_text = input().strip()
            note.edit_text(new_text)
            print(Fore.GREEN + "✅ Нотатку оновлено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Редагування тегів у нотатці
    elif action == "edit" and len(parts) >= 3 and parts[1] == "tag":
        title = parts[2]

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound(title)

            note = notebook.get_note(index)

            print("Нові теги через пробіл: ", end="")
            tags = input().strip().split()
            note.replace_tags(tags)
            print(Fore.GREEN + "✅ Теги оновлено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Видалення тегу з нотатки
    elif action == "delete" and len(parts) >= 4 and parts[1] == "tag":
        title = parts[2]
        tag_to_delete = parts[3]

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound(title)

            note = notebook.get_note(index)
            note.delete_tags(tag_to_delete)
            print(Fore.GREEN + f"🗑️ Тег '{tag_to_delete}' видалено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Видалення нотатки
    elif action == "delete" and len(parts) >= 3 and parts[1] == "note":
        title = parts[2]

        try:
            notebook.delete_note_by_title(title)
            print(Fore.GREEN + f"🗑️ Нотатку '{title}' видалено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Пошук нотатки
    elif action == "search" and len(parts) >= 3 and parts[1] == "note":
        keyword = " ".join(parts[2:])
        results = notebook.search(keyword)

        for n in results:
            print(n)

    # Показ усіх нотаток
    elif command == "show all notes":
        for note in notebook.notes():
            print(note)

    # Сортування нотаток за тегами
    elif command == "sort notes by tag":
        notes = notebook.notes(order="tags")

        for n in notes:
            print(n)

    # Невідома команда
    else:
        print(Fore.RED + "⚠️ Невідома команда для нотаток.")