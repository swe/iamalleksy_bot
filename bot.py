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
from buttonsfunctions import buttonone, buttontwo


# Put the token that you received from BotFather in the quotes
bot = Bot(token="")

# Initializing the dispatcher object
dp = Dispatcher(bot)

# Creating the reply keyboards
keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("🌍 Add new location", "💰 Check your assets")
locationkeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("📍 Send location", "Back")

# Handling the /start and /help commands
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # Sending a greeting message that includes the reply keyboard
    greeting = message.from_user.first_name
    await asyncio.sleep(1.0)
    await message.answer(f"Hello {greeting}! What would you like me to do for you today?", reply_markup=keyboard_reply)

# Handling location button

@dp.message_handler()
async def check_rp(message: types.Message):

    if message.text == '🌍 Add new location':
        # Responding with a message for the first button
        await message.reply("It looks like you're travelling! Isn't it gorgeous?")
        await asyncio.sleep(1.0)
        await message.answer("Just send me your current location, and I will add it to your map with visited places.",
                             reply_markup=locationkeyboard)

# Handling assets button
    elif message.text == '💰 Check your assets':
        # Responding with a message for the second button
        buttontwo()
        response = buttontwo()
        await message.answer(response)

    else:
        # Responding with a message that includes the text of the user's message
        await message.reply("I can not understand this command. Please, use /help to find what I can do.")

# Starting the bot

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)