from aiogram import types

from database.commands import create_user
from keyboards.buttons import start_button


async def say_hello(message: types.Message):
    await message.answer('Здравствуйте, заполните данные для оплаты занятий с преподавателем',
                         reply_markup=await start_button())
    await create_user(user_id=message.from_user.id, username=message.from_user.username,
                      fullname=message.from_user.full_name)
