"""
note_commands.py — модуль для обробки команд нотаток у CLI-застосунку.

Забезпечує додавання, редагування, пошук, сортування, видалення нотаток та тегів
у межах об'єкта NoteBook.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import shlex
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
    try:
        parts = shlex.split(command.strip())
    except ValueError:
        # If shlex parsing fails, fall back to regular split
        parts = command.strip().split()

    if not parts:
        print(Fore.RED + "⚠️ Порожня команда.")
        return

    action = parts[0].lower()

    # Додавання нової нотатки
    if action == "add" and len(parts) >= 3 and parts[1] == "note":
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
        # Handle multiword titles with quotes
        if len(parts) == 3:
            title = parts[2].strip('"')
        else:
            # Join all parts from index 2 onwards and strip quotes
            title = " ".join(parts[2:]).strip('"')

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound()

            index, note = notebook.get_note(index)

            print("Новий текст нотатки: ", end="")
            new_text = input().strip()
            note.edit_text(new_text)
            print(Fore.GREEN + "✅ Нотатку оновлено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Редагування тегів у нотатці
    elif action == "edit" and len(parts) >= 3 and parts[1] == "tag":
        # Handle multiword titles with quotes
        if len(parts) == 3:
            title = parts[2].strip('"')
        else:
            # Join all parts from index 2 onwards and strip quotes
            title = " ".join(parts[2:]).strip('"')

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound()

            index, note = notebook.get_note(index)

            print("Нові теги через пробіл: ", end="")
            tags = input().strip().split()
            note.replace_tags(tags)
            print(Fore.GREEN + "✅ Теги оновлено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Видалення тегу з нотатки
    elif action == "delete" and len(parts) >= 4 and parts[1] == "tag":
        # Handle multiword titles with quotes
        # If title is quoted, it will be a single element after shlex parsing
        # If title is unquoted multiword, we need to join elements until the last one (which is the tag)
        if len(parts) == 4:
            # Simple case: delete tag "title" tag or delete tag title tag
            title = parts[2].strip('"')
            tag_to_delete = parts[3]
        else:
            # Complex case: delete tag multiword title tag
            # The last element is the tag, everything from index 2 to -1 is the title
            title = " ".join(parts[2:-1]).strip('"')
            tag_to_delete = parts[-1]

        try:
            index = notebook.find_note_index_by_title(title)
            if index is None:
                raise NoteNotFound()

            index, note = notebook.get_note(index)
            note.delete_tags(tag_to_delete)
            print(Fore.GREEN + f"🗑️ Тег '{tag_to_delete}' видалено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Видалення нотатки
    elif action == "delete" and len(parts) >= 3 and parts[1] == "note":
        # Handle multiword titles with quotes
        if len(parts) == 3:
            title = parts[2].strip('"')
        else:
            # Join all parts from index 2 onwards and strip quotes
            title = " ".join(parts[2:]).strip('"')

        try:
            notebook.delete_note_by_title(title)
            print(Fore.GREEN + f"🗑️ Нотатку '{title}' видалено.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    # Пошук нотатки
    elif action == "search" and len(parts) >= 3 and parts[1] == "note":
        keyword = " ".join(parts[2:])
        results = notebook.search(keyword)

        for index, note in results:
            print(note)

    # Показ усіх нотаток
    elif command == "show all notes":
        for index, note in notebook.notes():
            print(note)

    # Сортування нотаток за тегами
    elif command == "sort notes by tag":
        notes = notebook.notes(order=NoteBook.SortOrder.tags)

        for index, note in notes:
            print(note)

    # Невідома команда
    else:
        print(Fore.RED + "⚠️ Невідома команда для нотаток.")