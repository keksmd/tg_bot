from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup


def verify_itmo_id_markup(telegram_id: int, itmo_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    verify_button = InlineKeyboardButton('Все верно', callback_data=f'verify_{telegram_id}_{itmo_id}')
    cancel_button = InlineKeyboardButton('Отказать', callback_data=f'cancel_{telegram_id}_{itmo_id}')
    markup.add(verify_button, cancel_button)
    return markup


def main_keyboard():
    # вместо new_meeting и get_bonus может быть написано что угодно
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    new_meeting = KeyboardButton('Узнать про новые события')
    get_bonus = KeyboardButton('Получить бонус')
    markup.add(new_meeting, get_bonus)
    return markup
