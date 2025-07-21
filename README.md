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
├── requirements.txt                     # phonenumbers==9.0.9, colorama==0.4.6
└── .gitignore                           # Стандартні виключення (venv, __pycache__, .DS_Store)
```

## Робота в команді

Команда реалізовує проєкт у реальному робочому середовищі з використанням:
-  Git/GitHub — [репозиторій проєкту](https://github.com/darinav/project-v4noznti/)
- Trello — [дошка завдань](https://trello.com/b/zo3BC7Op/vi4nozayniatiproject)
- Презентація [гугл презентація] (https://onedrive.live.com/edit?id=E4D7F5D8F7B5A1D3!152&resid=E4D7F5D8F7B5A1D3!152&authkey=!ADtOr_eFWL0aepY&ithint=file,pptx&e=3b5D8u&wdo=2&cid=e4d7f5d8f7b5a1d3 )

## 🧩 Функціонал

### 📇 Адресна книга
- Додавання нового контакту з:
  - ім'ям
  - телефоном
  - email
  - адресою
  - днем народження
- Додавання кількох телефонів, email, адрес
- Редагування контакту
- Пошук контактів за ключовим словом
- Видалення контакту
- Перегляд усіх контактів
- Показати дні народження протягом N днів

### 🗒️ Нотатки
- Додавання нотаток з:
  - заголовком
  - текстом
  - тегами (витягуються автоматично або редагуються вручну)
- Редагування тексту нотатки
- Редагування тегів
- Видалення тегу з нотатки
- Видалення нотатки
- Пошук нотатки за заголовком
- Перегляд усіх нотаток
- Сортування нотаток за тегами

---

## 💻 Команди CLI

### 📇 Контакти
```
add contact <name>
edit contact <name>
show contact <name>
delete contact <name>
show all contacts
show birthdays <days>
search contact <keyword>
```

### 🗒️ Нотатки
```
add note "<title>" "<text>"
edit note <title>
edit tag <title>
delete tag <title> <tag>
delete note <title>
search note <title>
show all notes
sort notes by tag
```

### 🔁 Загальні
```
switch            - перемкнутися між адресною книгою та нотатками
help              - показати доступні команди
exit / close      - вийти із застосунку
```

## 🎨 Кольори (інтерфейс)
- 📇 Контакт: `Fore.BLUE`
- 📞 Телефон: `Fore.YELLOW`
- 🏠 Адреса: `Fore.GREEN`
- 📧 Email: `Fore.CYAN`
- 🎂 День народження: `Fore.RED`
- 🏷️ Теги: `Fore.BLUE`

## 🛠️ Технічні деталі

- Python >= 3.10
- Основні бібліотеки:
  - `datetime` — робота з датами та днями народження
  - `re` — регулярні вирази для пошуку тегів та валідації email
  - `collections` — `UserDict` як база для книг
  - `colorama` — кольоровий інтерфейс CLI
  - `phonenumbers` — валідація телефонних номерів
  - `enum`, `abc`, `typing` — допоміжні модулі Python


## 📦 Залежності
```
colorama
phonenumbers
```


## ▶️ Запуск
```bash
python cli.py
```

## ▶️ Встановлення та запуск
Після клонування проєкту його можна встановити як звичайний Python‑пакет:
```bash
pip install .
```

Після інсталяції консольний помічник доступний по команді:
```bash
assistant
```

## 📎 Примітка
Усі дані зберігаються локально (через серіалізацію об'єктів).