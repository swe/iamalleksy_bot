#!venv/bin/python

# Importing required libraries
import logging
import asyncio
import yaml
import telegram
import requests
import json

import aiogram.utils.markdown as fmt

from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from functions/locationHandler import cityJsonDecoder
from test import getlocationdata

# Additional functions of the bot
# from buttonsfunctions import buttonone, buttontwo
#from functions/startMenu import coordinates2city

# Put the token that you received from BotFather in the quotes
bot = Bot(token="")

# Initializing the dispatcher object
dp = Dispatcher(bot)

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
    # Initializing message with first name
    greeting = message.from_user.first_name
    # Sending a greeting message that includes the reply keyboard
    await message.answer(f"👋🏻")
    await asyncio.sleep(1.0)
    await message.answer(f"Hello {greeting}! What would you like me to do for you today?", reply_markup=intro_reply)


@dp.message_handler(Text(contains="🌍 Add new location"))
async def with_puree(message: types.Message):
    locationBtn = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    LocationBtn = types.KeyboardButton("📍 Share Location", request_location=True)
    locationBtn.add(LocationBtn)

    await message.answer("Wow! Are you travelling somewhere?")
    await message.answer("Please, share your new location, where you are now", reply_markup=locationBtn)


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def on_location(message: types.Message):
    # location = message.location
    lat = message.location.latitude
    lon = message.location.longitude

    getlocationdata(lat, lon)

    # await message.answer(f"Thank you for sharing your location! You are at {yourcity}).")


@dp.message_handler(Text(contains="💰 Check your assets"))
async def with_puree(message: types.Message):
    await message.answer("Monies!")

    def get_wallet_balance():
        api_url = f"https://toncenter.com/api/v2/getAddressBalance?address="
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                balance = response.json().get("result")
                return balance
            else:
                return None
        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None

    balance = get_wallet_balance()
    if balance is not None:
        print(f"Your TON wallet balance is: {balance} TON")
    else:
        print("Failed to retrieve the wallet balance.")



# Starting the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)