"""
command_suggestions.py — модуль для пропозиції найближчих команд користувачу.

Використовує difflib для знаходження найбільш схожих команд на основі введеного тексту.
"""

import difflib
from typing import List, Tuple


class CommandSuggester:
    """Клас для пропозиції команд на основі схожості з введеним текстом."""
    
    def __init__(self):
        """Ініціалізує списки доступних команд для контактів та нотаток."""
        self.contact_commands = [
            "add contact",
            "edit contact", 
            "delete contact",
            "show contact",
            "show all contacts",
            "show birthdays",
            "search contact"
        ]
        
        self.note_commands = [
            "add note",
            "edit note",
            "edit tag", 
            "delete tag",
            "delete note",
            "search note",
            "show all notes",
            "sort notes by tag"
        ]
        
        self.general_commands = [
            "switch",
            "switch 1", 
            "switch 2",
            "help",
            "exit",
            "close"
        ]
    
    def get_suggestions(self, user_input: str, mode: str = "contact", max_suggestions: int = 3) -> List[str]:
        """
        Знаходить найближчі команди до введеного користувачем тексту.
        
        Args:
            user_input (str): текст, введений користувачем
            mode (str): режим роботи ("contact" або "note")
            max_suggestions (int): максимальна кількість пропозицій
            
        Returns:
            List[str]: список найближчих команд
        """
        if mode == "contact":
            available_commands = self.contact_commands + self.general_commands
        elif mode == "note":
            available_commands = self.note_commands + self.general_commands
        else:
            available_commands = self.contact_commands + self.note_commands + self.general_commands
        
        # Використовуємо difflib для знаходження найближчих збігів
        suggestions = difflib.get_close_matches(
            user_input.lower().strip(),
            [cmd.lower() for cmd in available_commands],
            n=max_suggestions,
            cutoff=0.3  # мінімальна схожість 30%
        )
        
        # Повертаємо оригінальні команди (з правильним регістром)
        result = []
        for suggestion in suggestions:
            for cmd in available_commands:
                if cmd.lower() == suggestion:
                    result.append(cmd)
                    break
        
        return result
    
    def get_partial_suggestions(self, user_input: str, mode: str = "contact", max_suggestions: int = 3) -> List[str]:
        """
        Знаходить команди, які починаються з введеного тексту або містять його.
        
        Args:
            user_input (str): текст, введений користувачем
            mode (str): режим роботи ("contact" або "note")
            max_suggestions (int): максимальна кількість пропозицій
            
        Returns:
            List[str]: список команд, що містять введений текст
        """
        if mode == "contact":
            available_commands = self.contact_commands + self.general_commands
        elif mode == "note":
            available_commands = self.note_commands + self.general_commands
        else:
            available_commands = self.contact_commands + self.note_commands + self.general_commands
        
        user_lower = user_input.lower().strip()
        
        # Спочатку шукаємо команди, що починаються з введеного тексту
        starts_with = [cmd for cmd in available_commands if cmd.lower().startswith(user_lower)]
        
        # Потім шукаємо команди, що містять введений текст
        contains = [cmd for cmd in available_commands 
                   if user_lower in cmd.lower() and cmd not in starts_with]
        
        # Об'єднуємо результати, віддаючи пріоритет тим, що починаються з тексту
        result = starts_with + contains
        
        return result[:max_suggestions]
    
    def get_best_suggestion(self, user_input: str, mode: str = "contact") -> str:
        """
        Знаходить найкращу (найближчу) команду до введеного користувачем тексту.
        
        Args:
            user_input (str): текст, введений користувачем
            mode (str): режим роботи ("contact" або "note")
            
        Returns:
            str: найкраща команда або None якщо нічого не знайдено
        """
        # Спочатку пробуємо часткові збіги (вони мають вищий пріоритет)
        partial_suggestions = self.get_partial_suggestions(user_input, mode, 1)
        
        if partial_suggestions:
            return partial_suggestions[0]
        
        # Якщо часткових збігів немає, пробуємо difflib
        suggestions = self.get_suggestions(user_input, mode, 1)
        
        if suggestions:
            return suggestions[0]
        
        return None

    def suggest_command_interactive(self, user_input: str, mode: str = "contact") -> tuple:
        """
        Генерує повідомлення з найкращою пропозицією команди та інтерактивним підтвердженням.
        
        Args:
            user_input (str): текст, введений користувачем
            mode (str): режим роботи ("contact" або "note")
            
        Returns:
            tuple: (suggestion_message, suggested_command) або (error_message, None)
        """
        best_suggestion = self.get_best_suggestion(user_input, mode)
        
        if best_suggestion:
            if mode == "contact":
                base_msg = "⚠️ Невідома команда для контактів."
            else:
                base_msg = "⚠️ Невідома команда для нотаток."
            
            suggestion_msg = f"{base_msg} Можливо, ви мали на увазі: '{best_suggestion}'? (y/n)"
            return suggestion_msg, best_suggestion
        
        # Якщо нічого не знайдено, повертаємо стандартне повідомлення
        if mode == "contact":
            return "⚠️ Невідома команда для контактів.", None
        else:
            return "⚠️ Невідома команда для нотаток.", None

    def suggest_command(self, user_input: str, mode: str = "contact") -> str:
        """
        Генерує повідомлення з пропозиціями команд для користувача.
        
        Args:
            user_input (str): текст, введений користувачем
            mode (str): режим роботи ("contact" або "note")
            
        Returns:
            str: повідомлення з пропозиціями або стандартне повідомлення про помилку
        """
        # Спочатку пробуємо часткові збіги
        partial_suggestions = self.get_partial_suggestions(user_input, mode, 2)
        
        if partial_suggestions:
            if mode == "contact":
                base_msg = "⚠️ Невідома команда для контактів."
            else:
                base_msg = "⚠️ Невідома команда для нотаток."
            
            suggestions_text = ", ".join([f"'{cmd}'" for cmd in partial_suggestions])
            return f"{base_msg} Можливо, ви мали на увазі: {suggestions_text}?"
        
        # Якщо часткових збігів немає, пробуємо difflib
        suggestions = self.get_suggestions(user_input, mode, 2)
        
        if suggestions:
            if mode == "contact":
                base_msg = "⚠️ Невідома команда для контактів."
            else:
                base_msg = "⚠️ Невідома команда для нотаток."
            
            suggestions_text = ", ".join([f"'{cmd}'" for cmd in suggestions])
            return f"{base_msg} Можливо, ви мали на увазі: {suggestions_text}?"
        
        # Якщо нічого не знайдено, повертаємо стандартне повідомлення
        if mode == "contact":
            return "⚠️ Невідома команда для контактів."
        else:
            return "⚠️ Невідома команда для нотаток."


# Глобальний екземпляр для використання в інших модулях
command_suggester = CommandSuggester()