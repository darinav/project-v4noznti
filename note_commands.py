"""
note_commands.py — модуль для обробки команд нотаток у CLI-застосунку.

Забезпечує додавання, редагування, пошук, сортування, видалення нотаток та тегів
у межах об'єкта NoteBook.
"""

from colorama import Fore
from books import NoteBook, Note
from books.note_book.book import NoteBook as FullNoteBook
NoteBook.SortOrder = FullNoteBook.SortOrder

def _find_note_exact(notebook: NoteBook, title: str):
    notes = [item for item in notebook.notes() if item[1].title == title]
    return notes[0] if notes else None

def _print_notes_table(notes: list[Note]):
    headers = [
        "Назва",
        "Текст",
        "Теги"
    ]
    rows = [[n.title, n.text, n.tags] for n in notes]
    if not rows:
        print(Fore.YELLOW + "Немає нотаток для виводу.")
        return

    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + rows))]
    def fmt_row(row):
        return " │ ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))

    border = "─┼─".join("─" * w for w in col_widths)

    print(Fore.CYAN + fmt_row(headers))
    print(Fore.MAGENTA + border)
    for row in rows:
        print(fmt_row(row))

def handle_note_command(command: str, notebook: NoteBook):
    parts = command.strip().split()

    if not parts:
        print(Fore.RED + "⚠️ Порожня команда.")
        return

    action = parts[0].lower()

    if action == "add" and len(parts) >= 2 and parts[1] == "note":
        if len(parts) == 2:
            title = input("Введіть назву нотатки: ").strip()
            if not title:
                print(Fore.RED + "⚠️ Назва не може бути порожньою.")
                return
            text = input("Введіть текст нотатки: ").strip()
            if not text:
                print(Fore.RED + "⚠️ Текст не може бути порожнім.")
                return
        elif len(parts) == 3:
            title = parts[2].strip('"')
            text = input("Введіть текст нотатки: ").strip()
            if not text:
                print(Fore.RED + "⚠️ Текст не може бути порожнім.")
                return
        else:
            title = parts[2].strip('"')
            text = " ".join(parts[3:]).strip('"')

        try:
            note = Note(title, text)
            notebook.add_note(note)
            print(Fore.GREEN + f"✅ Нотатку '{title}' додано.")
        except Exception as e:
            print(Fore.RED + f"❌ Помилка: {e}")

    elif action == "edit" and len(parts) >= 2 and parts[1] == "note":
        if len(parts) == 2:
            title = input("Введіть назву нотатки для редагування: ").strip()
            if not title:
                print(Fore.RED + "⚠️ Назва не може бути порожньою.")
                return
        else:
            title = parts[2]

        found = _find_note_exact(notebook, title)
        if not found:
            print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
            return
        index, note = found
        new_text = input("Новий текст нотатки: ").strip()
        note.edit_text(new_text)
        print(Fore.GREEN + "✅ Нотатку оновлено.")

    elif action == "edit" and len(parts) >= 2 and parts[1] == "tag":
        if len(parts) == 2:
            title = input("Введіть назву нотатки для редагування тегів: ").strip()
            if not title:
                print(Fore.RED + "⚠️ Назва не може бути порожньою.")
                return
        else:
            title = parts[2]

        found = _find_note_exact(notebook, title)
        if not found:
            print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
            return
        index, note = found
        tags_input = input("Нові теги через пробіл: ").strip()
        tags = tags_input.split() if tags_input else []
        note.replace_tags(*tags)
        print(Fore.GREEN + "✅ Теги оновлено.")

    elif action == "delete" and len(parts) >= 2 and parts[1] == "tag":
        if len(parts) == 2:
            title = input("Введіть назву нотатки для видалення тегу: ").strip()
            if not title:
                print(Fore.RED + "⚠️ Назва не може бути порожньою.")
                return

            found = _find_note_exact(notebook, title)
            if not found:
                print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
                return

            tag_to_delete = input("Введіть тег для видалення: ").strip()
            if not tag_to_delete:
                print(Fore.RED + "⚠️ Тег не може бути порожнім.")
                return

        elif len(parts) == 3:
            title = parts[2]
            found = _find_note_exact(notebook, title)
            if not found:
                print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
                return

            tag_to_delete = input("Введіть тег для видалення: ").strip()
            if not tag_to_delete:
                print(Fore.RED + "⚠️ Тег не може бути порожнім.")
                return

        else:
            title = parts[2]
            tag_to_delete = parts[3]
            found = _find_note_exact(notebook, title)
            if not found:
                print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
                return

        index, note = found
        if tag_to_delete not in note.tags_list:
            print(Fore.YELLOW + f"⚠️ Тег '{tag_to_delete}' не знайдено у нотатці.")
        else:
            note.delete_tags(tag_to_delete)
            print(Fore.GREEN + f"🗑️ Тег '{tag_to_delete}' видалено.")

    elif action == "delete" and len(parts) >= 2 and parts[1] == "note":
        if len(parts) == 2:
            title = input("Введіть назву нотатки для видалення: ").strip()
            if not title:
                print(Fore.RED + "⚠️ Назва не може бути порожньою.")
                return
        else:
            title = parts[2]

        found = _find_note_exact(notebook, title)
        if not found:
            print(Fore.RED + f"❌ Нотатку з назвою '{title}' не знайдено.")
            return
        index, _ = found
        notebook.delete_note(index)
        print(Fore.GREEN + f"🗑️ Нотатку '{title}' видалено.")

    elif action == "search" and len(parts) >= 2 and parts[1] == "note":
        if len(parts) == 2:
            keyword = input("Введіть фразу для пошуку: ").strip()
            if not keyword:
                print(Fore.RED + "⚠️ Пошуковий запит не може бути порожнім.")
                return
        else:
            keyword = " ".join(parts[2:])
        notes = notebook.search(keyword)
        _print_notes_table([note for _, note in notes])

    elif command == "show all notes":
        _print_notes_table([note for _, note in notebook.notes()])

    elif command == "sort notes by tag":
        notes = notebook.notes(order=NoteBook.SortOrder.tags)
        _print_notes_table([note for _, note in notes])

    else:
        print(Fore.RED + "⚠️ Невідома команда для нотаток.")
