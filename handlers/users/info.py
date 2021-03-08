from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('info'))
async def info_contact(message: types.Message):
    await message.answer('Для связи и предложений\n'
                         'email: rozhkin.m@gmail.com\n'
                         'telegram: @michaelrozhkin')