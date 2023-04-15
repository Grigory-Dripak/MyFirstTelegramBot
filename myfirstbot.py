import telebot
from os import getenv
from dotenv import load_dotenv, find_dotenv
import extensions

calc = extensions.CurrencyConverter()

load_dotenv(find_dotenv())
# @mypersonal85_bot
bot = telebot.TeleBot(getenv('TOKEN'))


@bot.message_handler(content_types=['photo'])
def chating(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username}, nice meme XDD")


@bot.message_handler(commands=['start', 'help'])
def trycommand(message: telebot.types.Message):
    bot.reply_to(message, f"Привет, {message.chat.username}! Для пересчета валют используй выражение в следующем формате:\n"
                          f"<исходная валюта> <целевая валюта> <количество валюты>\n "
                          f"Для вывода спиская доступных валют используй команду /values")

@bot.message_handler(commands=['values'])
def trycommand(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username}, я могу конвертировать следующие валюты: \n "
                          f"{', '.join(extensions.legal_currency)}")

@bot.message_handler()
def trycommand(message: telebot.types.Message):
    try:
        base, quote, amount = calc.textnormalize(message.text)
        text = calc.get_price(base, quote, amount)
    except extensions.APIException as e:
        bot.reply_to(message, f'Ошибка ввода параметров для перевода валюты: \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка выполнения программы: \n {e}')
    else:
        bot.reply_to(message, text)

bot.polling(none_stop=True)