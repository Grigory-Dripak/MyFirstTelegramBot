import telebot
from time import time
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = telebot.TeleBot(getenv('TOKEN'))


@bot.message_handler(content_types=['photo'])
def chating(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username}, nice meme XDD")


@bot.message_handler(commands=['start', 'help'])
def trycommand(message: telebot.types.Message):
    print('command' + message.text)
    bot.reply_to(message, f"Привет, {message.chat.username}! Могу пересчитать валюты.")

@bot.message_handler()
def trycommand(message: telebot.types.Message):
    print(message.text)
    bot.reply_to(message, f"Hello {message.chat.username}")

bot.polling(none_stop=True)