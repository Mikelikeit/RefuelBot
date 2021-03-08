from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


choice1 = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='Начать заправку')
    ],

], resize_keyboard=True)

choice2 = ReplyKeyboardMarkup([
    [
      KeyboardButton(text='Редактировать')
    ],
    [
        KeyboardButton(text='Завершить')
    ]

], resize_keyboard=True)

choice3 = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='Статистика')
    ],
    [
        KeyboardButton(text='/start')
    ]

], resize_keyboard=True)

choice4 = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='Мои заправки')
    ],
    [
        KeyboardButton(text='Общие данные')
    ],
    [
        KeyboardButton(text='/start')
    ]

], resize_keyboard=True)

