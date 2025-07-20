import difflib
from cli.guess_command.possible_commands import GENERAL_COMMANDS

def _suggest_command(user_input: str, valid_commands: list[str], cutoff: float = 0.6) -> str | None:
    if not user_input or not valid_commands:
        return None
    matches = difflib.get_close_matches(user_input, valid_commands, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def _is_general_command(cmd: str) -> bool:
    return cmd.lower() in [c.lower() for c in GENERAL_COMMANDS]

def _find_best_match(command, valid_commands):
    parts = command.split()
    base_cmd = ' '.join(parts[:2]).lower() if len(parts) > 1 else parts[0].lower() if parts else ""
    candidates = [' '.join(c.split()[:2]).lower() if len(c.split()) > 1 else c.split()[0].lower()
                  for c in valid_commands]
    suggestion = _suggest_command(base_cmd, candidates)
    if not suggestion or base_cmd == suggestion:
        for cmd in valid_commands:
            if cmd.lower().startswith(command.lower()) and cmd.lower() != command.lower():
                return cmd
        typo = _suggest_command(command.lower(), [cmd.lower() for cmd in valid_commands])
        if typo:
            for cmd in valid_commands:
                if cmd.lower() == typo:
                    return cmd
    else:
        for cmd in valid_commands:
            cmd_base = ' '.join(cmd.split()[:2]).lower() if len(cmd.split()) > 1 else cmd.split()[0].lower()
            if cmd_base == suggestion:
                return cmd
    return None

def handle_command_with_guess(command, valid_commands, handler, *handler_args, general_command_callback=None):
    # Спец-обробка: якщо команда починається з "show birthdays" — завжди приймаємо це як валідну команду
    if command.lower().startswith("show birthdays"):
        handler(command, *handler_args)
        return

    best_match = _find_best_match(command, valid_commands)
    if best_match and best_match.lower() != command.lower():
        print(f"Можливо, ви мали на увазі: '{best_match}'? (y/n)")
        if input().strip().lower() == "y":
            command = best_match
            if _is_general_command(command):
                if general_command_callback:
                    return general_command_callback(command)
                return
        else:
            print("⚠️ Невідома команда для контактів.")
            return
    if _is_general_command(command):
        if general_command_callback:
            return general_command_callback(command)
        return
    handler(command, *handler_args)