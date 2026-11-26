# Personal Assistant

Консольний персональний помічник: адресна книга та нотатки.
Командний проєкт курсу GoIT Python Core.

## Можливості

- Контакти: імʼя, адреса, телефони, email, день народження.
- Додавання, пошук, редагування та видалення контактів.
- Перевірка телефону та email під час введення.
- Список контактів, у яких день народження через N днів.
- Нотатки: додавання, пошук, редагування, видалення.
- Збереження всіх даних на диск у папці користувача.

> Розділи будуть доповнюватися в міру готовності функцій.

## Встановлення

Потрібен Python 3.10 або новіший.

```bash
git clone https://github.com/DemiD223/personal-assistant.git
cd personal-assistant
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Команди

| Команда | Опис |
|---|---|
| `hello` | Привітання |
| `add <імʼя> <телефон>` | Додати контакт або телефон до нього |
| `change <імʼя> <старий> <новий>` | Змінити телефон |
| `phone <імʼя>` | Показати телефони контакту |
| `all` | Показати всі контакти |
| `help` | Показати список команд |
| `exit` / `close` | Вийти з програми |

## Структура проєкту

```
personal-assistant/
├── main.py                 # точка входу
└── assistant/
    ├── contacts/           # Field, Name, Phone, Record, AddressBook
    ├── notes/              # Note, NoteBook
    ├── storage/            # збереження та завантаження даних
    └── cli/                # цикл команд, обробники, input_error
```

## Команда

| Роль | Учасник |
|---|---|
| Тімлід | [@DemiD223](https://github.com/DemiD223) |
| Скрам-майстер | |
| Розробник 1 | [@BullseyeProg](https://github.com/BullseyeProg) |
| Розробник 2 | [@DemiD223](https://github.com/DemiD223) |
| Розробник 3 | |

Правила роботи з репозиторієм — у файлі [CONTRIBUTING.md](CONTRIBUTING.md).
