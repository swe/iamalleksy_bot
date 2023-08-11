#!venv/bin/python
import logging
import asyncio
import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# Importing required libraries
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from buttonsfunctions import buttonone, buttontwo

# Put the token that you received from BotFather in the quotes
bot = Bot(token="***")

# Initializing the dispatcher object
dp = Dispatcher(bot)

# Creating the reply keyboard
keyboard_reply = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add("🌍 Add new location", "💰 Check your assets")

# Handling the /start and /help commands
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    # Sending a greeting message that includes the reply keyboard
    await message.answer("Hello! how are you?", reply_markup=keyboard_reply)


# Handling all other messages
@dp.message_handler()
async def check_rp(message: types.Message):

    if message.text == '🌍 Add new location':
        # Responding with a message for the first button
        await message.reply("Hi! this is first reply keyboards button.")
        buttonone()


    elif message.text == '💰 Check your assets':
        # Responding with a message for the second button
        await message.reply("Hi! this is second reply keyboards button.")
        buttontwo()

    else:
        # Responding with a message that includes the text of the user's message
        await message.reply("I can not understand this command. Please, use /help to find what I can do.")

# Starting the bot

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)