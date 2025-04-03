import os
import json
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Это твой личный финансовый бот. Готов отслеживать выплаты и давать медальки!")

def status(update: Update, context: CallbackContext):
    data = load_data()
    выполнено = data.get("выполнено", 0)
    всего = data.get("всего", 9)
    процент = int((выполнено / всего) * 100)
    бар = "█" * выполнено + "░" * (всего - выполнено)
    msg = f"Прогресс:\n[{бар}] {выполнено}/{всего} — {процент}%"
    update.message.reply_text(msg)

def коллекция(update: Update, context: CallbackContext):
    medals = {
        "апрель": "april.png",
        "июнь": "june.png",
        "июль": "july.png",
        "декабрь": "december.png"
    }
    for month, file in medals.items():
        try:
            with open(f"medals/{file}", "rb") as img:
                update.message.reply_photo(photo=img, caption=f"Медаль за {month.capitalize()}")
        except:
            update.message.reply_text(f"Медаль за {month.capitalize()} не найдена.")

def получил_зарплату(update: Update, context: CallbackContext):
    data = load_data()
    month = context.args[0] if context.args else "апрель"  # Используем аргумент, если он есть
    if month not in data["месяцы"]:
        data["месяцы"][month] = {
            "расходы": False,
            "бюджет": False,
            "платежи": False
        }
        save_data(data)
    update.message.reply_text(f"Зарплата получена за {month}! Проверьте, все ли выплаты по этому месяцу выполнены.")

def отметить(update: Update, context: CallbackContext):
    month = context.args[0] if context.args else "апрель"
    item = context.args[1] if len(context.args) > 1 else "расходы"
    data = load_data()
    if month in data["месяцы"]:
        data["месяцы"][month][item] = True
        save_data(data)
        update.message.reply_text(f"Отметили {item} за {month}.")
    else:
        update.message.reply_text(f"Месяц {month} не найден.")

def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("статус", status))
    dp.add_handler(CommandHandler("коллекция", коллекция))
    dp.add_handler(CommandHandler("получил_зарплату", получил_зарплату))
    dp.add_handler(CommandHandler("отметить", отметить))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
