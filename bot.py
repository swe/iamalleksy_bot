#!venv/bin/python
import logging
import asyncio
import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

bot = Bot(token="***")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
