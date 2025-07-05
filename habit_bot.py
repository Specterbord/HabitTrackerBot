from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os
from datetime import datetime, timedelta
import asyncio
import nest_asyncio

DATA_FILE = 'habit_data.json'
REMINDERS_FILE = 'reminders.json'

# Загрузка/сохранение данных привычек
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id):
    data = load_data()
    return data.get(str(user_id), {})

def update_user_data(user_id, user_data):
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)

# Загрузка/сохранение напоминаний
def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return {}
    with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я — твой бот-трекер привычек.\n"
        "📌 Команды:\n"
        "/add <название> — добавить привычку\n"
        "/habits — список привычек\n"
        "/done <название> — отметить выполненной\n"
        "/status — прогресс\n"
        "/reset <название> — сбросить привычку\n"
        "/remind HH:MM — установить напоминание (например, /remind 08:00)"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    if not context.args:
        await update.message.reply_text("❗ Укажи название привычки после /add")
        return

    habit_name = ' '.join(context.args).strip().lower()
    if habit_name in user_data:
        await update.message.reply_text("⚠️ Такая привычка уже есть.")
        return

    user_data[habit_name] = {"streak": 0, "last_done": ""}
    update_user_data(user_id, user_data)
    await update.message.reply_text(f"✅ Привычка '{habit_name}' добавлена!")

async def habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        await update.message.reply_text("❗ У тебя пока нет привычек. Добавь через /add")
        return
    msg = '\n'.join([f"• {h}" for h in user_data.keys()])
    await update.message.reply_text(f"📋 Твои привычки:\n{msg}")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    if not context.args:
        await update.message.reply_text("❗ Укажи привычку после /done")
        return

    habit_name = ' '.join(context.args).strip().lower()
    if habit_name not in user_data:
        await update.message.reply_text("⚠️ Такой привычки нет.")
        return

    today = datetime.now().strftime('%Y-%m-%d')
    last_done = user_data[habit_name]['last_done']

    if last_done == today:
        await update.message.reply_text("✅ Ты уже отмечал эту привычку сегодня.")
        return

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    user_data[habit_name]['streak'] = (
        user_data[habit_name]['streak'] + 1 if last_done == yesterday else 1
    )
    user_data[habit_name]['last_done'] = today
    update_user_data(user_id, user_data)

    await update.message.reply_text(
        f"🎉 Привычка '{habit_name}' выполнена!\n🔥 Стрик: {user_data[habit_name]['streak']} дней подряд"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        await update.message.reply_text("❗ Добавь привычки через /add")
        return

    msg = "📈 Прогресс:\n"
    for habit, info in user_data.items():
        msg += f"• {habit}: {info['streak']} дней подряд\n"
    await update.message.reply_text(msg)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    if not context.args:
        await update.message.reply_text("❗ Укажи привычку для сброса.")
        return

    habit_name = ' '.join(context.args).strip().lower()
    if habit_name not in user_data:
        await update.message.reply_text("⚠️ Такой привычки нет.")
        return

    user_data[habit_name] = {"streak": 0, "last_done": ""}
    update_user_data(user_id, user_data)
    await update.message.reply_text(f"🔄 Привычка '{habit_name}' сброшена.")

# Напоминания
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if not context.args:
        await update.message.reply_text("❗ Формат: /remind 08:00")
        return

    try:
        hour, minute = map(int, context.args[0].split(':'))
        reminders = load_reminders()
        reminders[user_id] = f"{hour:02}:{minute:02}"
        save_reminders(reminders)
        await update.message.reply_text(f"🔔 Напоминание установлено на {hour:02}:{minute:02}")
    except:
        await update.message.reply_text("❗ Неверный формат. Пиши вот так: /remind 08:00")

# Цикл, отправляющий напоминания
async def send_reminders(app):
    while True:
        now = datetime.now().strftime("%H:%M")
        reminders = load_reminders()
        for user_id, time_str in reminders.items():
            if time_str == now:
                try:
                    await app.bot.send_message(chat_id=int(user_id), text="🔔 Напоминание: не забудь выполнить свою привычку!")
                except Exception:
                    pass
        await asyncio.sleep(60)

# Запуск
async def main():
    app = ApplicationBuilder().token("7697417191:AAGwE5yjwbXu6PiRgvD1OCiNqeQElZUo9_8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("habits", habits))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("remind", remind))

    asyncio.create_task(send_reminders(app))
    print("🤖 Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())


