import os
import subprocess

from telebot import TeleBot

import config
from user_service import UserService
from database import SessionFactory
from markups import *


bot = TeleBot('7503351084:AAFISVpV2EMBmuTjRVbsqdMVyDeBPGRsUNU')
user_service = UserService(SessionFactory)


@bot.message_handler(commands=['start'])
def handle_start(message):
    text = '''
    Привет. Это бот для впн факультета СУиР. Отправь свой itmo_id (Только цифры)
    '''
    user = user_service.get_by_telegram_id(message.chat.id)
    if not user:
        user_service.create_user(message.chat.id, message.from_user.username)
    answer = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(answer, handle_itmo_id)


def handle_itmo_id(message):
    username = message.from_user.username
    telegram_id = message.from_user.id
    try:
        itmo_id = int(message.text)
        if user_service.get_by_itmo_id(itmo_id):
            bot.reply_to(message, 'Этот itmo_id уже привязан к другому аккаунту')
        bot.reply_to(message, 'Ваш itmo_id отпрвлен на модерацию')
        admins = user_service.get_admins()
        text_to_admin = f'''
        Подтвердите пользователя @{username}\n
        Он указал itmo_id {itmo_id}
        '''
        for admin in admins:
            bot.send_message(admin.telegram_id,
                             text_to_admin,
                             reply_markup=verify_itmo_id_markup(telegram_id, itmo_id))
    except:
        bot.reply_to(message, 'Неверный itmo_id')


@bot.callback_query_handler(func=lambda call: call.data.startswith('verify'))
def handle_verification_confirm(call):
    params = call.data.split('_')[1:]
    telegram_id = params[0]
    itmo_id = params[1]
    try:
        if user_service.is_verified(telegram_id):
            bot.send_message(call.from_user.id, 'Этот пользователь уже подтвержден')
            return
        user = user_service.verify_user(telegram_id, itmo_id)
        if user.verified:
            bot.send_message(call.from_user.id, 'Пользователь подтвержден!')
            bot.send_message(telegram_id, 'Ваш аккаунт успешно подтвержден!', reply_markup=main_keyboard())
            bot.delete_message(call.from_user.id, call.message.id)
    except Exception as e:
        bot.reply_to(call.from_user.id, f'Произошла ошибка: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel'))
def cancel_verification(call):
    params = call.data.split('_')[1:]
    telegram_id = params[0]
    itmo_id = params[1]
    bot.send_message(telegram_id, f'Веривикация отклонена.\n'
                                  f'Возможно itmo_id, который ты указал ({itmo_id}), неверный\n'
                                  f'Попробуй снова через команду /start')
    bot.send_message(call.from_user.id, 'Заявка отклонена')
    bot.delete_message(call.from_user.id, call.message.id)


def send_vpn_files(message):
    telegram_id = message.from_user.id
    user = user_service.get_by_telegram_id(telegram_id)
    if user.verified:
        itmo_id = user.itmo_id
        try:
            file_paths = []
            for i in range(1, 5):
                profile_name = f"{itmo_id}_{i}"
                config_file_path = os.path.join(config.config_directory, f"{profile_name}.ovpn")

                if not os.path.exists(config_file_path):
                    subprocess.run(['pivpn', 'add', '-n', profile_name, 'nopass', '-d', '3560'], check=True)

                file_paths.append(config_file_path)

            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as config_file:
                        bot.send_document(message.chat.id, config_file)
                else:
                    bot.reply_to(message, f"Файл конфигурации {file_path} не найден.")

        except subprocess.CalledProcessError:
            bot.reply_to(message,
                         "Произошла ошибка при генерации файла конфигурации.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}")
    else:
        bot.send_message(telegram_id, 'Ваш профиль не подтвержден')


def send_instruction(message):
    bot.send_message(message.chat.id, 'Установи приложуху и вставь туда файлы')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text == 'Получить файлы для VPN':
        send_vpn_files(message)
        return
    if text == 'Инструкция по подключению':
        send_instruction(message)
        return

try:
    bot.polling()
except:
    ...