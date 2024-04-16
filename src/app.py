import telebot

TOKEN = "7021553373:AAGi5s3Y7oLJkUkUA3QGOaLEzlb1UXJcb0o"
CHANNEL_ID = ""

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """
Привет! Я бот для налоговых льгот!
Напиши мне любой регион, а я в ответ
Расскажу тебе про вычеты и выдам секрет,
Как с инвестициями сэкономить бюджет!
""")


@bot.message_handler()
def resend_message_to_channel(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    # https://github.com/eternnoir/pyTelegramBotAPI/issues/1259
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
