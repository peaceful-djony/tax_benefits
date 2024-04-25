import telebot
import pandas as pd
from Levenshtein import distance as levenshtein_distance

from bcolors import Bcolors
import config
from regions import regions


TOKEN = config.TOKEN
PATH_TO_DATA = "./data/rostelecom.xlsx"

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
    search_res = find_region(message.text.lower())
    if not search_res:
        msg = "Такой регион пока не поддерживается. Попробуй ещё раз!"
        bot.send_message(message.chat.id, msg)
        return

    requested_region = df[df['Name_lower'] == search_res]
    region = requested_region['Субъект Российской Федерации'].values[0]
    result = requested_region[2024].values[0]

    res_msg = "положен." if result == "ДА" else "не положен."
    # извлекаем информацию из ячеек с остальной информацией
    norm_act = requested_region['Закон ИНВ'].values[0]
    max_amount = requested_region['Максимальный размер вычета'].values[0]
    rate = requested_region['Ставка для исчисления предельной величины'].values[0]

    if not pd.isnull(max_amount):
        res_msg += f"\nМаксимальный размер вычета: {max_amount}"
    if not pd.isnull(rate):
        res_msg += f"\nСтавка для исчисления предельной величины: {rate}"
    if not pd.isnull(norm_act):
        res_msg += f"\nРегламентирующих закон: {norm_act}"
    bot.send_message(message.chat.id, f'В регионе \"{region}\" за 2024 год вычет: {res_msg}')


def prepare_data(data):
    # добавили столбец, в котором названия регионов будут в нижнем регистре
    data['Name_lower_primary'] = data['Субъект Российской Федерации'].str.lower()
    to_replace = '|'.join(['область', 'республика', 'автономный', 'край', 'округ'])
    # делаем столбец без области, края и т.п.
    data['Name_lower'] = (data['Name_lower_primary']
                          .str.replace(to_replace, '').str.strip())


def find_region(input_name):
    """
    Функция для поиска региона с учетом опечаток
    """
    input_name = input_name.lower().strip()
    best_match = None
    min_distance = float('inf')

    for region, aliases in regions.items():
        # Проверяем совпадение с полным названием
        dist = levenshtein_distance(input_name, region)
        if dist < min_distance:
            min_distance = dist
            best_match = region

        # Проверяем совпадение с сокращениями
        for alias in aliases:
            dist = levenshtein_distance(input_name, alias)
            if dist < min_distance:
                min_distance = dist
                best_match = region

    # Возвращаем наилучшее совпадение, если расстояние Левенштейна не слишком велико
    return best_match if min_distance <= len(input_name) // 2 else None


def check_region():
    not_found_regions = []
    for reg in df['Name_lower_primary']:
        r = regions.get(reg, None)
        if not r:
            not_found_regions.append(reg)

    if not_found_regions:
        print(f'{Bcolors.WARNING}Не найдены следующие регионы: {not_found_regions}{Bcolors.WARNING}')
    else:
        print(f'{Bcolors.OKGREEN}Все регионы найдены!{Bcolors.ENDC}')


if __name__ == '__main__':
    df = pd.read_excel(PATH_TO_DATA,
                       skiprows=1,
                       usecols='A:L',
                       nrows=89,
                       )
    prepare_data(df)

    check_region()

    # https://github.com/eternnoir/pyTelegramBotAPI/issues/1259
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
