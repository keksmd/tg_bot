import telebot
from telebot import TeleBot
import json
import requests

from markups import main_keyboard

BOT_TOKEN = '7771331841:AAHVsoCzizNKzFoYvnWMwsHcNcMGfJux7Ko'
bot = TeleBot(BOT_TOKEN)
SERVER_URL = 'https://my-json-server.typicode.com/typicode/demo/profile'  # Замените на ваш URL

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_keyboard())

# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     try:
#         response = requests.get(SERVER_URL)
#         response.raise_for_status()
#         data = response.json()
#
#         # Обработка ответа и вывод пользователю.
#         # Пример, предполагающий что data - это словарь с ключом "result"
#         try:
#             result = data['result']
#             bot.reply_to(message, f"Ответ от сервера: {result}")
#         except KeyError:
#             bot.reply_to(message, f"Ответ от сервера: {data}") #Если нет ключа "result", выводим все данные
#
#
#     except requests.exceptions.RequestException as e:
#         bot.reply_to(message, f"Ошибка при запросе к серверу: {e}")
#     except json.JSONDecodeError as e:
#         bot.reply_to(message, f"Ошибка при обработке ответа сервера: {e}")
#     except KeyError as e:
#         bot.reply_to(message, f"Ошибка: Не найден необходимый ключ в ответе сервера: {e}")
#     except Exception as e: #Обработка других исключений
#         bot.reply_to(message, f"Произошла непредвиденная ошибка: {e}")


bot.polling()