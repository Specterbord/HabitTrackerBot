# HabitTrackerBot
 A Telegram bot that helps you build and maintain healthy habits. Track your daily progress and stay consistent with your routines
 Features
- `/start` — Welcome message and usage instructions  
- `/add <habit>` — Add a new habit  
- `/habits` — View your list of habits  
- `/done <habit>` — Mark a habit as completed for today  
- `/status` — Check your current streaks  
- `/reset <habit>` — Reset progress for a specific habit  
Technologies Used

- Python 3.11+
- Library: [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) (v20.3)
- Data Storage: Local `JSON` file (`habit_data.json`)
- How to Run

1. Install dependencies:
   pip install python-telegram-bot==20.3
Replace the placeholder token in habit_bot.py:

python
token("YOUR_BOT_TOKEN_HERE")
with your own token from BotFather
Launch the bot:
python habit_bot.py
📁 Project Structure
HabitTrackerBot/
├── habit_bot.py       # Main Telegram bot script
├── habit_data.json    # User habit progress data
└── README.md          # Project documentation
👤 Author
Developed with ❤️ by a high school student as part of a personal portfolio for international university applications.
GitHub: @Specterbord
