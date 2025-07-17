from books import NoteBook, Note
from books.note_book.error import NoteNotFound, NoteAlreadyExist, NoteTitleMandatory, NoteTextMandatory
from colorama import Fore, Style

def handle_note_command(command: str, note_book: NoteBook):
    try:
        if command.startswith("add note "):
            parts = command[len("add note "):].strip()
            if parts.startswith('"'):
                split = parts.split('"')
                if len(split) >= 4:
                    title = split[1].strip()
                    text = split[3].strip()
                    note = Note(title, text)
                    note_book.add_note(note)
                    print(Fore.GREEN + f"📝 Нотатку '{title}' додано.")
                    return
            print(Fore.RED + "⚠️ Формат: add note \"<title>\" \"<text>\"")

        elif command.startswith("search note "):
            title = command[len("search note "):].strip()
            note = note_book.find(title)
            print(Fore.YELLOW + str(note))

        elif command.startswith("delete note "):
            title = command[len("delete note "):].strip()
            note_book.delete_note(title)
            print(Fore.YELLOW + f"🗑️ Нотатку '{title}' видалено.")

        elif command.startswith("edit note "):
            title = command[len("edit note "):].strip()
            note = note_book.find(title)
            new_text = input("📝 Введіть новий текст нотатки: ").strip()
            if new_text:
                note.edit_text(new_text)
                print(Fore.GREEN + f"✅ Нотатку '{title}' оновлено.")
            else:
                print(Fore.RED + "⚠️ Текст не може бути порожнім")

        elif command.startswith("edit tag "):
            title = command[len("edit tag "):].strip()
            note = note_book.find(title)
            new_tags = input("🏷️ Введіть нові теги через пробіл: ").strip()
            note.edit_tags(new_tags)
            print(Fore.GREEN + f"🏷️ Теги нотатки '{title}' оновлено.")

        elif command.startswith("delete tag "):
            parts = command[len("delete tag "):].strip().split(maxsplit=1)
            if len(parts) != 2:
                print(Fore.RED + "⚠️ Формат: delete tag <title> <tag>")
                return
            title, tag = parts[0], parts[1]
            note = note_book.find(title)
            note.remove_tag(tag)
            print(Fore.YELLOW + f"🗑️ Тег '{Fore.BLUE + tag + Fore.YELLOW}' видалено з нотатки '{title}'")

        elif command == "show all notes":
            notes = note_book.notes()
            if not notes:
                print("📭 Немає нотаток.")
            for note in notes:
                print(Fore.YELLOW + str(note))

        elif command == "sort notes by tag":
            notes = note_book.notes(order=NoteBook.SortOrder.tags)
            if not notes:
                print("📭 Немає нотаток для сортування.")
            for note in notes:
                print(Fore.YELLOW + str(note))

        else:
            print(Fore.RED + "⚠️ Команда для нотаток не розпізнана.")

    except (NoteNotFound, NoteAlreadyExist, NoteTitleMandatory, NoteTextMandatory) as e:
        print(Fore.RED + f"⚠️ {e}")
    except Exception as e:
        print(Fore.RED + f"❌ Виникла помилка: {e}")
