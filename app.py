# Телеграмм-бот для конвертации валют: @valuta_course_bot
import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def function_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Добро пожаловать,\t {message.chat.username}!')
    bot.send_message(message.chat.id, 'Это бот для конвертации валют.')
    bot.send_message(message.chat.id, 'Для начала работы воспользуйтесь подсказками бота /help')

@bot.message_handler(commands=['help'])
def function_help(message: telebot.types.Message):
    text = 'Для конвертации введите 3 параметра через пробел:\n' \
'<Ваша валюта>\n<В какую валюту хотите перевести>\n' \
'<Количество переводимой валюты>\n' \
'(пример: рубль евро 1000)\n' \
'Обратите внимание - название валюты пишется\nв именительном падеже единственного числа!\n' \
'Посмотреть список доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите три параметра через пробел или\nвоспользуйтесь подсказками бота /help')

        val_origin, val_base, amount = values

        val_origin = val_origin.lower()
        val_base = val_base.lower()

        total_base = CurrencyConverter.get_price(val_origin, val_base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {val_origin} = {round((total_base * float(amount)), 2)} {val_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)





