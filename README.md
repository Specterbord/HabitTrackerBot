# HabitTrackerBot
🤖 Telegram-бот для отслеживания привычек. Помогает формировать полезные привычки и не сбиваться с пути.

🚀 Возможности
/start — приветствие и инструкция

/add <название> — добавить новую привычку

/habits — список всех привычек

/done <название> — отметить привычку выполненной

/status — посмотреть текущий прогресс (стрик)

/reset <название> — сбросить привычку

🧠 Технологии
Python 3.11+

Библиотека: python-telegram-bot v20.3

Хранение данных в habit_data.json

⚙️ Как запустить
Установи зависимости:

pip install python-telegram-bot==20.3
В файле habit_bot.py замени:

python
token("YOUR_BOT_TOKEN_HERE")
на свой токен из BotFather

Запусти:

python habit_bot.py
📁 Структура проекта
bash
Копировать
Редактировать
HabitTrackerBot/
├── habit_bot.py       # Основной код бота
├── habit_data.json    # Хранилище данных привычек
└── README.md          # Документация
Автор
Разработано с ❤️ студентом для портфолио
GitHub: @Specterbord

