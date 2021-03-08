from aiogram.dispatcher.filters.state import StatesGroup, State


class Refuel(StatesGroup):
    id_state = State()
    date_state = State()
    price_state = State()
    liters_state = State()
    mileage_state = State()

