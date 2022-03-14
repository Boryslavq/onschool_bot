from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

price_list = CallbackData('pay', 'name', 'bill_id', 'price')


async def start_button() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Регистрация")
        ]
    ]

    kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return kb


async def _skip() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Пропустить', callback_data='skip'))
    return kb


async def to_pay() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Перейти к оплате', callback_data='choose'))
    return kb


async def choose_tarif():
    kb = InlineKeyboardMarkup(row_width=1)
    prices = [900, 1000, 1200, 1500]
    for price in prices:
        kb.insert(InlineKeyboardButton(text=f"{price} рублей", callback_data=f'{price}'))

    kb.insert(InlineKeyboardButton(text='Произвольная сумма', callback_data='any'))

    return kb


async def way_to_pay() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Юкасса', callback_data='youcassa')).add(
        InlineKeyboardButton(text='QiWi', callback_data='qiwi'))
    return kb


async def qiwi_menu(url: str, price: int, bill="") -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.insert(InlineKeyboardButton(text="Оплатить", url=url)).insert(
        InlineKeyboardButton(text="Проверить оплату",
                             callback_data=price_list.new(name='qiwi', bill_id=bill, price=price)))
    return kb


async def yoo_menu(url: str, price: int, bill="") -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.insert(InlineKeyboardButton(text="Оплатить", url=url)).insert(
        InlineKeyboardButton(text="Проверить оплату",
                             callback_data=price_list.new(name='yoo', bill_id=bill, price=price)))
    return kb
