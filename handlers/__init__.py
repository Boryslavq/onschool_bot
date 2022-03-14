from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from handlers.form import start_form, set_email, set_phone, create_log, choose_pay, qiwi_pay, check_qiwi_pay, \
    choose_price, ucassa_pay, check_yoo, any_sum
from handlers.start import say_hello
from keyboards.buttons import price_list
from states import states


def setup(dp: Dispatcher):
    dp.register_message_handler(say_hello, CommandStart())
    dp.register_message_handler(start_form, text='Регистрация')
    dp.register_message_handler(set_email, state=states.Form.fullname)
    dp.register_message_handler(set_phone, state=states.Form.email)
    dp.register_message_handler(set_email, state=states.Form.fullname)

    dp.register_callback_query_handler(create_log, text='skip', state=states.Form.phone)
    dp.register_message_handler(create_log, state=states.Form.phone)
    dp.register_callback_query_handler(check_qiwi_pay, price_list.filter(name='qiwi'))
    dp.register_callback_query_handler(check_yoo, price_list.filter(name='yoo'))
    dp.register_message_handler(choose_pay, state=states.SetPrice.price, content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(choose_price, text='choose')
    dp.register_callback_query_handler(any_sum, text='any')
    dp.register_callback_query_handler(choose_pay, regexp='\d{1,4}')
    # qiwi payment
    dp.register_callback_query_handler(qiwi_pay, text='qiwi', state='*')
    # yoocassa payment
    dp.register_callback_query_handler(ucassa_pay, text='youcassa', state='*')
    # dp.register_pre_checkout_query_handler(process_pre_checkout_query)
    # dp.register_message_handler(process_pay, content_types=ContentType.SUCCESSFUL_PAYMENT)
