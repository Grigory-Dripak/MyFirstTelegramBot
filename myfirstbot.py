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
    bot.reply_to(message, f"{message.chat.username}, я могу конвертировать следующие валюты: \n"
                          f"{', '.join([i for i in calc.legal_currency.values()])}")

@bot.message_handler()
def trycommand(message: telebot.types.Message):
    print(message.text)
    bot.reply_to(message, f"Hello {message.chat.username}")

if __name__ == "__main__":
    bot.polling(none_stop=True)