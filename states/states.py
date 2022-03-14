from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    fullname = State()
    email = State()
    phone = State()


class SetPrice(StatesGroup):
    price = State()



