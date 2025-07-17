import difflib

CONTACT_COMMANDS = [
    "add contact",
    "show contact",
    "delete contact",
    "show all contacts",
    "show birthdays",
    "search contact",
]

NOTE_COMMANDS = [
    "add note",
    "search note",
    "delete note",
    "show all notes",
    "sort notes by tag",
]

def __suggest_command(user_input: str, valid_commands: list[str], cutoff: float = 0.6) -> str | None:
    if not user_input or not valid_commands:
        return None
    matches = difflib.get_close_matches(user_input, valid_commands, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def handle_command_with_guess(command, valid_commands, handler, *handler_args):
    parts = command.lower().split()
    base_cmd = ' '.join(parts[:2]) if len(parts) > 1 else parts[0] if parts else ""

    base_valid_commands = [
        ' '.join(c.split()[:2]) if len(c.split()) > 1 else c.split()[0]
        for c in valid_commands
    ]
    suggestion = __suggest_command(base_cmd, base_valid_commands)
    if suggestion and not base_cmd.startswith(suggestion):
        print(f"Можливо, ви мали на увазі: '{suggestion}'? (y/n)")
        if input().strip().lower() == "y":
            rest = ' '.join(parts[2:]) if len(parts) > 2 else ""
            command = f"{suggestion} {rest}".strip()
            handler(command, *handler_args)
        else:
            print("Команда не розпізнана.")
    else:
        handler(command, *handler_args)
