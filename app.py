import telebot

TOKEN = "7021553373:AAGi5s3Y7oLJkUkUA3QGOaLEzlb1UXJcb0o"
CHANNEL_ID = ""

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """
Вечер в хату!
Часик в радость, чифир в сладость, ногам ходу, голове приходу. Матушку удачу, сто тузов по сдаче

❗️ Зачем меня создали?

Чтобы распилить государственные бабки!!!

❓ Что я делаю?

Не знаю, но делаю я это лучше всех!
""")


@bot.message_handler(commands=['svetlana'])
def send_svetlana_message(message):
    bot.send_message(message.chat.id, "test")


@bot.message_handler()
def resend_message_to_channel(message):
    bot.send_message(CHANNEL_ID, message.text)


if __name__ == '__main__':
    # https://github.com/eternnoir/pyTelegramBotAPI/issues/1259
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
