from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from . import logging


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
