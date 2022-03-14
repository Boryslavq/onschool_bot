import random
from typing import Union
from uuid import uuid4
from aiogram import types
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P
from yoomoney import Quickpay

from data import config
from database.commands import add_bill_id, get_bill_id, add_info, get_info
from handlers.helpers import check_num, check_email, check
from google_api.sheets import create_record
from keyboards.buttons import _skip, to_pay, way_to_pay, qiwi_menu, choose_tarif, yoo_menu, start_button
from states import states

p2p = QiwiP2P(config.QIWI_TOKEN)


async def start_form(message: types.Message):
    await message.answer('Введите своё имя')
    await states.Form.fullname.set()


async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer('Введите своё email')
    await states.Form.email.set()


async def set_phone(message: types.Message, state: FSMContext):
    status = await check_email(message.text)
    if status:
        await state.update_data(email=message.text)
        await message.answer('Введите свой номер телефона', reply_markup=await _skip())
        await states.Form.phone.set()
    else:
        await message.answer('Невалидный email, попробуйте ещё раз')


async def create_log(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    if isinstance(message, types.Message):
        if await check_num(message.text):
            await state.update_data(phone=message.text)
            async with state.proxy() as data:
                fullname = data.get('fullname')
                email = data.get('email')
                phone = data.get('phone')
                await add_info(user_id=message.from_user.id, full_name=fullname, gmail=email, phone=phone)
                await message.answer('Ваша заявка:\n'
                                     f'Имя: {fullname}\n'
                                     f'Email: {email}\n'
                                     f'Телефон: {phone}', reply_markup=await to_pay())
            await state.finish()

        else:
            await message.answer('Введите правильный номер')
    elif isinstance(message, types.CallbackQuery):
        async with state.proxy() as data:
            call = message
            fullname = data.get('fullname')
            email = data.get('email')
            await add_info(user_id=message.from_user.id, full_name=fullname, gmail=email)
            await call.message.edit_text('Ваша заявка:\n'
                                         f'Имя: {fullname}\n'
                                         f'Email: {email}', reply_markup=await to_pay())
        await state.finish()


async def choose_price(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите тариф', reply_markup=await choose_tarif())


async def any_sum(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите произвольную сумму')
    await states.SetPrice.price.set()


async def choose_pay(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    msg = 'Выберите способ оплаты'
    if isinstance(message, types.Message):
        if message.text.isdigit():
            await state.update_data(price=message.text)
            await message.answer(msg, reply_markup=await way_to_pay())
        else:
            await message.answer('Введите число')
    elif isinstance(message, types.CallbackQuery):
        callback = message
        await state.update_data(price=callback.data)
        await callback.message.edit_text(msg, reply_markup=await way_to_pay())


async def ucassa_pay(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        price = int(data.get('price'))
    num = str(uuid4())
    quickpay = Quickpay(
        receiver="410019858243597",
        quickpay_form="shop",
        targets="Оплата курса",
        paymentType="SB",
        sum=price,
        label=num
    )
    await add_bill_id(user_id=callback.from_user.id, bill=num)
    await callback.message.edit_text(
        'Ваша ссылка на оплату \n\nВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату»',
        reply_markup=await yoo_menu(url=quickpay.redirected_url, price=price, bill=num))
    await state.finish()


async def check_yoo(callback: types.CallbackQuery, callback_data: dict):
    bill = callback_data.get('bill_id')
    price = callback_data.get('price')
    if await get_bill_id(callback.from_user.id, bill):
        if await check(bill):
            await callback.message.delete()
            await callback.message.answer('Поздравляю, вы оплатили счёт', reply_markup=await start_button())
            info = await get_info(callback.from_user.id)
            await create_record(user_id=callback.from_user.id, price=price, gmail=info.gmail,
                                full_name=info.full_name,
                                phone=info.phone)
        else:
            await callback.answer('Вы не оплатили счёт')
    else:
        await callback.message.answer('Платёж не найден')


async def qiwi_pay(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        price = int(data.get('price'))
    num = str(uuid4())
    bill = p2p.bill(bill_id=num, amount=price, lifetime=15, comment=num[5:random.randrange(10, 15)])
    await add_bill_id(user_id=callback.from_user.id, bill=num)
    await callback.message.edit_text(
        'Ваш счёт для оплаты\n\nВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату»',
        reply_markup=await qiwi_menu(url=bill.pay_url, bill=bill.bill_id, price=price))
    await state.finish()


async def check_qiwi_pay(callback: types.CallbackQuery, callback_data: dict):
    bill = callback_data.get('bill_id')
    price = callback_data.get('price')
    if get_bill_id(callback.from_user.id, bill):
        if str(p2p.check(bill_id=bill).status) == "PAID":
            await callback.message.delete()
            await callback.message.answer('Поздравляю, вы оплатили счёт', reply_markup=await start_button())
            info = await get_info(callback.from_user.id)
            await create_record(user_id=callback.from_user.id, price=price, gmail=info.gmail,
                                full_name=info.full_name,
                                phone=info.phone)
        else:
            await callback.answer('Вы не оплатили счёт')
    else:
        await callback.message.answer('Платёж не найден')
