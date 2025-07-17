# Персональний помічник (Final Project - project-v4noznti)

## 📌 Опис проєкту

Цей проєкт розроблено в рамках завершального етапу курсу **Python Programming: Foundations and Best Practices** у **GoIT Neoversity**.  
Мета проєкту — застосувати отримані знання та навички Python у командній роботі, створивши повноцінний застосунок — **Персональний помічник** для керування контактами та нотатками з інтерфейсом командного рядка.

Проєкт є не лише технічним викликом, але й чудовою можливістю для учасників спробувати себе в ролі Team Lead, розробника, тестувальника, координатора — і навчитись ефективній командній співпраці, плануванню та презентації результатів.

## Структура проекту

```
project-v4noznti/
├── books/
│   ├── __init__.py
│   ├── commons/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── field.py
│   ├── address_book/
│   │   ├── __init__.py
│   │   ├── book.py                      # AddressBook: додавання, пошук, дні народження, пошук по всіх полях
│   │   ├── error/
│   │   │   ├── __init__.py
│   │   │   └── exceptions.py            # ContactNotFound, ContactAlreadyExist тощо
│   │   └── record/
│   │       ├── __init__.py
│   │       └── record.py                # Клас Record з Name, Phones, Emails, Address, Birthday
│   └── note_book/
│       ├── __init__.py
│       ├── book.py                      # NoteBook: додавання, пошук, сортування нотаток
│       ├── error/
│       │   ├── __init__.py
│       │   └── exceptions.py            # NoteNotFound, NoteAlreadyExist, TagValueCannotBeEmpty тощо
│       └── note/
│           ├── __init__.py
│           └── note.py                  # Клас Note з Title, Text, Tags, автоматичне витягування тегів
│
├── cli.py                               # Основний CLI-інтерфейс (input, виклик функцій з books)
├── contact_commands.py                  # Команди для AddressBook
├── note_commands.py                     # Команди для NoteBook
├── __init__.py                          # Метадані про проєкт
├── README.md                            # Інструкція, опис команд
├── requirements.txt                     # phonenumbers==9.0.9
└── .gitignore                           # Стандартні виключення (venv, __pycache__, .DS_Store)
```

## Основні функції

### Контакти:
- Зберігання контактів з іменами, адресами, телефонами, email та днями народження
- Перевірка коректності введення номера телефону та email
- Пошук, редагування, видалення контактів
- Виведення контактів з днями народження у найближчі дні

### Нотатки:
- Додавання текстових нотаток
- Редагування, видалення, пошук нотаток
- Використання **тегів** для опису теми нотатки
- Пошук і сортування нотаток за тегами

### Збереження даних:
- Дані зберігаються на диску у форматі, що дозволяє відновити інформацію при повторному запуску

## Додатковий функціонал

- Інтелектуальний аналіз запиту користувача: розпізнавання наміру та пропозиція відповідної команди
- Можливість розширення функцій, кастомізації та масштабування

## Робота в команді

Команда реалізовує проєкт у реальному робочому середовищі з використанням:
-  Git/GitHub — [репозиторій проєкту](https://github.com/darinav/project-v4noznti/)
- Trello — [дошка завдань](https://trello.com/b/zo3BC7Op/vi4nozayniatiproject)
- Презентація - [гугл диск] ()

## 🛠️ Технічні деталі

- Python 3.10+
- Модулі: `datetime`, `re`, `collections`, `pathlib`, `phonenumbers`

## 📦 Залежності
```
colorama
phonenumbers
```

## ▶️ Запуск
```bash
python cli.py
```

## 🎨 Кольори (інтерфейс)
- 📇 Контакт: `Fore.BLUE`
- 📞 Телефон: `Fore.YELLOW`
- 🏠 Адреса: `Fore.GREEN`
- 📧 Email: `Fore.CYAN`
- 🎂 День народження: `Fore.RED`
- 🏷️ Теги: `Fore.BLUE`




### 🔁 Загальні
```
switch                             - перемкнутися між адресною книгою та нотатками
help                               - показати доступні команди
exit / close                       - вийти із застосунку
```

### 📇 Контакти
```
add contact <name>                 - створити контакт (з інтерактивним введенням даних)
edit contact <name>                - редагувати контакт
show contact <name>                - переглянути контакт
delete contact <name>              - видалити контакт
show all contacts                  - список усіх контактів
show birthdays <days>              - дні народження через N днів
search contact <keyword>           - пошук контактів
```

### 🗒️ Нотатки
```
add note "<title>" "<text>"        - додати нотатку
edit note <title>                  - редагувати текст нотатки
edit tag <title>                   - змінити теги
delete tag <title> <tag>           - видалити тег із нотатки
delete note <title>                - видалити нотатку
search note <title>                - пошук нотатки
show all notes                     - перегляд усіх нотаток
sort notes by tag                  - сортування за тегами
```


