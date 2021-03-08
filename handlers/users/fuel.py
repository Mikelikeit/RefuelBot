from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.choice_buttons import choice1, choice2, choice3, choice4
from loader import dp, db
from states import Refuel


@dp.message_handler(Command('start'))
async def start_writing(message: types.Message):
    await message.answer(text=f'Привет {message.from_user.full_name}! Выберите действие', reply_markup=choice1)
    await Refuel.id_state.set()


@dp.message_handler(state=Refuel.id_state)
async def get_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(id_state=user_id)
    await message.answer('Введите сумму на которую заправились', reply_markup=ReplyKeyboardRemove())
    await Refuel.price_state.set()


@dp.message_handler(state=Refuel.price_state)
async def get_price(message: types.Message, state: FSMContext):
    try:
        if float(message.text) >= 0:
            price = float(message.text)
        else:
            await message.answer('Вы ввели отрицательное число! Поробуйте еще раз.')
    except ValueError:
        await message.answer('Вы ввели не число! Попробуйте еще раз.')
    await state.update_data(price_state=price)
    await message.answer('Введите количество литров')
    await Refuel.liters_state.set()


@dp.message_handler(state=Refuel.liters_state)
async def get_liters(message: types.Message, state: FSMContext):
    try:
        if float(message.text) >= 0:
            liters = float(message.text)
        else:
            ('Вы ввели отрицательное число! Поробуйте еще раз.')
    except ValueError:
        await message.answer('Вы ввели не число! Попробуйте еще раз.')
    await state.update_data(liters_state=liters)
    await message.answer('Введите текущий пробег')
    await Refuel.mileage_state.set()


@dp.message_handler(state=Refuel.mileage_state)
async def get_mileage(message: types.Message, state: FSMContext):
    last_mileage = await db.select_last_five_refuels(user_id=message.from_user.id)
    print(len(last_mileage))
    try:
        if len(last_mileage) == 0 or int(message.text) > last_mileage[0][4]:
            mileage = abs(int(message.text))
        else:
            await message.answer('Ваш введеный пробег меньше текущего. Введите корректный пробег')
    except ValueError:
        await message.answer('Вы ввели не число! Попробуйте еще раз.')
    await state.update_data(mileage_state=mileage)
    await message.answer('Выберите действие', reply_markup=choice2)
    await state.reset_state(with_data=False)


@dp.message_handler(text='Редактировать')
async def edit_refuel(message: types.Message):
    await message.answer(f'Введите исправленные данные или повторите данные\n'
                         f'Первый ввод Цена\n'
                         f'Второй ввод Литры\n'
                         f'Тредий ввод Пробег', reply_markup=ReplyKeyboardRemove())
    await Refuel.price_state.set()


@dp.message_handler(state=Refuel.price_state)
async def edit_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    price = data.get('price_state')
    try:
        if float(message.text) >= 0:
            price = float(message.text)
        else:
            await message.answer('Вы ввели отрицательное число! Поробуйте еще раз.')
    except ValueError:
        await message.answer('Вы ввели не число! Попробуйте еще раз.')
    await state.update_data(price_state=price)
    await state.reset_state(with_data=False)


@dp.message_handler(text='Завершить')
async def finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('id_state')
    price = round(data.get('price_state'), 2)
    liters = round(data.get('liters_state'), 2)
    mileage = data.get('mileage_state')
    date = message.date
    per_liter = round(price / liters, 2)
    try:
        await db.add_user(user_id=user_id, user_name=message.from_user.full_name)
    except:
        pass
    await db.add_refuel(user_id=user_id, date=date, price=price, liters=liters, mileage=mileage, per_liter=per_liter)
    await message.answer(f'Вы завершили ввод. Ваша заправка:\n'
                         f'Дата: {date}\n'
                         f'Сумма: {price}\n'
                         f'Литры: {liters}\n'
                         f'Пробег: {mileage}\n'
                         f'Цена за литр: {per_liter}\n'
                         f'Для новых данных нажмите /start',
                         reply_markup=choice3)
    await state.finish()


@dp.message_handler(text='Статистика')
async def get_statistics(message: types.Message):
    await message.answer('Выберите действие', reply_markup=choice4)


@dp.message_handler(text='Мои заправки')
async def last_refuels(message: types.Message):
    all = await db.select_last_five_refuels(user_id=message.from_user.id)
    i = 0
    while i <= len(all):
        await message.answer(f'Ваша запрвка:\n'
                             f'Дата: {all[i][1]}\n'
                             f'Сумма: {round(all[i][2], 2)}\n'
                             f'Литры: {round(all[i][3], 2)}\n'
                             f'Пробег: {all[i][4]}\n'
                             f'Цена за литр: {round(all[i][2] / all[i][3], 2)}'
                             , reply_markup=choice4)
        i += 1


@dp.message_handler(text='Общие данные')
async def info_refuels(message: types.Message):
    max_per_liter = await db.select_max_per_liter(user_id=message.from_user.id)
    min_per_liter = await db.select_min_per_liter(user_id=message.from_user.id)
    count_refuels = await db.select_count_refuels(user_id=message.from_user.id)
    sum_price = await db.select_sum_price(user_id=message.from_user.id)
    await message.answer(f'MAX цена литра: {round(max_per_liter[0][0], 2)}\n'
                         f'MIN цена литра: {round(min_per_liter[0][0], 2)}\n'
                         f'Всего заправок: {count_refuels[0][0]}\n'
                         f'Общие затраты: {round(sum_price[0][0], 2)}\n'
                         f'Средняя заправка: {round(sum_price[0][0] / count_refuels[0][0], 2)}')
