import threading
from telebot import types

import functions

def main_keyboard():
    """Generates keyboards for main menu."""

    keyboard = types.InlineKeyboardMarkup()
    about_button = types.InlineKeyboardButton('О нас', callback_data = 'about')
    manager_button = types.InlineKeyboardButton('Менеджер', callback_data = 'manager')
    keyboard.add(about_button, manager_button)
    keyboard.add(types.InlineKeyboardButton('Условия работы', callback_data = 'rules'))
    keyboard.add(types.InlineKeyboardButton('Отправить товар на расчет', callback_data = 'calculate'))
    keyboard.add(types.InlineKeyboardButton('Скачать бланк заявки', callback_data = 'download'))
    keyboard.add(types.InlineKeyboardButton('Калькулятор доставки', callback_data = 'shipment'))

    return keyboard


def about_keyboard():
    """Generates keyboard for 'about' section."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Обзор нашего склада', callback_data = 'stocks'))
    keyboard.add(types.InlineKeyboardButton('Отзывы о нас', callback_data = 'reviews'))
    keyboard.add(types.InlineKeyboardButton('Социальные сети', callback_data = 'networks'))
    keyboard.add(types.InlineKeyboardButton('Наши адреса', callback_data = 'addresses'))
    keyboard.add(types.InlineKeyboardButton('Реквизиты компании', callback_data = 'details'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_main'))
    return keyboard
    

def networks_keyboard():
    """Generates keyboard with social media links."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Наш сайт', url = 'https://chinatravel-tk.ru/'))
    keyboard.add(types.InlineKeyboardButton('Мы в Instagram', url = 'https://instagram.com/china__trevel?igshid=YmMyMTA2M2Y='))
    keyboard.add(types.InlineKeyboardButton('Мы в VK', url = 'https://vk.com/chinatrevel'))
    keyboard.add(types.InlineKeyboardButton('Наш Telegram канал', url = 'https://t.me/china_travel_ru'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_about'))
    return keyboard


def addresses_keyboard():
    """Generates keyboard with addresses of stocks."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Гуанчжоу (основной)', callback_data = 'guangzhou'))
    keyboard.add(types.InlineKeyboardButton('Пекин (экспресс-доставка)', callback_data = 'beijing'))
    keyboard.add(types.InlineKeyboardButton('Адреса складов в Москве', callback_data = 'moscow'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_about'))
    return keyboard


def rules_keyboard():
    """Generates keyboard with terms of use."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Доставка и ее стоимость', callback_data = 'cost'))
    keyboard.add(types.InlineKeyboardButton('Условия по выкупу', callback_data = 'terms'))
    keyboard.add(types.InlineKeyboardButton('Poizon', callback_data = 'poizon'))
    keyboard.add(types.InlineKeyboardButton('Пополнение AliPay', callback_data = 'alipay'))
    keyboard.add(types.InlineKeyboardButton('Курсы юаня и доллара', callback_data = 'currency'))
    keyboard.add(types.InlineKeyboardButton('Шаблон договора', callback_data = 'contract'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_main'))
    return keyboard


def back_about_keyboard():
    """Generates keyboards with 'back to about section' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_about'))
    return keyboard


def back_addresses_keyboard():
    """Generates keyboards with 'back to addresses section' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_addresses'))
    return keyboard


def back_rules_keyboard():
    """Generates keyboards with 'back to rules section' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_rules'))
    return keyboard


def back_rules_delete_keyboard():
    """Generates keyboards with 'back to rules section' button that should delete previous message."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_rules_delete'))
    return keyboard


def manager_keyboard(manager_username, manager_name):
    """Generates keyboards with 'proceed to manager' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f'Чат с менеджером', url = f'https://t.me/{manager_username}'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_main'))
    return keyboard


def back_main_keyboard():
    """Generates keyboards with 'bact to main menu' button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_main'))
    return keyboard


def only_manager_keyboard(manager_username):
    """Generates keyboards with 'proceed to manager' button (only this one)."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f'Чат с менеджером', url = f'https://t.me/{manager_username}'))
    return keyboard


def back_main_delete_keyboard():
    """Generates keyboards with 'back to main' button that should delete previous message."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать другой вопрос', callback_data = 'another_question'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data = 'back_main_delete'))
    return keyboard


def reply_menu():
    """Generates reply menu buttons."""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    menu_button = types.KeyboardButton(f'📱 Меню')
    manager_button = types.KeyboardButton(f'👨‍💼 Менеджер')
    keyboard.add(menu_button, manager_button)
    return keyboard