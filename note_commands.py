from books import NoteBook, Note
from books.note_book.error import NoteNotFound, NoteAlreadyExist, NoteTitleMandatory, NoteTextMandatory

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
                    print(f"📝 Нотатку '{title}' додано.")
                    return
            print("⚠️ Формат: add note \"<title>\" \"<text>\"")

        elif command.startswith("search note "):
            title = command[len("search note "):].strip()
            note = note_book.find(title)
            print(note)

        elif command.startswith("delete note "):
            title = command[len("delete note "):].strip()
            note_book.delete_note(title)
            print(f"🗑️ Нотатку '{title}' видалено.")

        elif command == "show all notes":
            notes = note_book.notes()
            if not notes:
                print("📭 Немає нотаток.")
            for note in notes:
                print(note)

        elif command == "sort notes by tag":
            notes = note_book.notes(order=NoteBook.SortOrder.tags)
            if not notes:
                print("📭 Немає нотаток для сортування.")
            for note in notes:
                print(note)

        else:
            print("⚠️ Команда для нотаток не розпізнана.")

    except (NoteNotFound, NoteAlreadyExist, NoteTitleMandatory, NoteTextMandatory) as e:
        print(f"⚠️ {e}")
    except Exception as e:
        print(f"❌ Виникла помилка: {e}")