import telebot
import pandas as pd

TOKEN = "7021553373:AAGi5s3Y7oLJkUkUA3QGOaLEzlb1UXJcb0o"

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
    requested_region = df[df['Name_lower'].str.contains(message.text.lower())]
    if requested_region.empty:
        msg = "Такой регион пока не поддерживается. Попробуй ещё раз!"
        bot.send_message(message.chat.id, msg)
    else:
        region = requested_region['Субъект Российской Федерации'].values[0]
        result = requested_region[2024].values[0]
        res_msg = "положен" if result == "ДА" else "не положен"
        bot.send_message(message.chat.id, f'В регионе \"{region}\" за 2024 год вычет: {res_msg}')


def prepare_data(data):
    # добавили столбец, в котором названия регионов будут в нижнем регистре
    data['Name_lower_primary'] = data['Субъект Российской Федерации'].str.lower()
    to_replace = '|'.join(['область', 'республика', 'автономный', 'край', 'округ'])
    # делаем столбец без области, края и т.п.
    data['Name_lower'] = (data['Name_lower_primary']
                          .str.replace(to_replace, '').str.strip())


if __name__ == '__main__':
    import os

    print(os.getcwd())
    df = pd.read_excel('./data/rostelecom.xlsx',
                       skiprows=1,
                       usecols='A:L',
                       nrows=89,
                       )
    prepare_data(df)

    # https://github.com/eternnoir/pyTelegramBotAPI/issues/1259
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
