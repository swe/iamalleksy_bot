#!venv/bin/python

# Importing required libraries
import logging
import asyncio
import yaml
import telegram

import aiogram.utils.markdown as fmt

from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup

# Additional functions of the bot
#from buttonsfunctions import buttonone, buttontwo
#from startMenu import start

# Put the token that you received from BotFather in the quotes
bot = Bot(token="6640404904:AAEg996r2gM_zSwzet1Syk7jPcIWkDyIDvg")

# Initializing the dispatcher object
dp = Dispatcher(bot)

#Initializing all required variables
greeting = message.from_user.first_name

# Creating the intro keyboard
introBtns = [
    ["🎥 Rate new film/show"],
    ["📚 Rate new book"],
    ["🌍 Add new location"],
    ["💰 Check your assets"],
    ["🌟 Update wishlist"],
    ["💡 Add project idea"]
]
intro_reply = ReplyKeyboardMarkup(introBtns, resize_keyboard=False, one_time_keyboard=True)

# Handling the /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # Sending a greeting message that includes the reply keyboard
    await message.answer(f"👋🏻")
    await asyncio.sleep(1.0)
    await message.answer(f"Hello {greeting}! What would you like me to do for you today?", reply_markup=intro_reply)





# Starting the bot

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)