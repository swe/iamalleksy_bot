#!venv/bin/python

# Importing required libraries
import yaml
import asyncio
import json
import requests
import psycopg2

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text


def yaml_parser(file_name):
    with open(file_name, "r") as file:
        data = yaml.safe_load(file)
        botToken = data["iamalleksy_bot"]["botToken"]
        openCageAPIkey = data["iamalleksy_bot"]["openCageAPI"]
        bdName = data["iamalleksy_bot"]["postgresDB"]
        bdPassword = data["iamalleksy_bot"]["postgresKey"]
        bdUser = data["iamalleksy_bot"]["postgresName"]
        bdHost = data["iamalleksy_bot"]["postgresHost"]
    return botToken, openCageAPIkey, bdName, bdUser, bdHost, bdPassword


botToken, openCageAPIkey, bdName, bdUser, bdHost, bdPassword = yaml_parser(
    "secrets.yml"
)

bot = Bot(token=botToken)
dp = Dispatcher(bot)
introBtns = [
    ["🌍 New visited place"],
    ["🌟 Update wishlist"],
    ["💡 I have an idea"],
    ["📖 New travel notes"],
    ["💰 Check your crypto"],
]
intro_reply = ReplyKeyboardMarkup(
    introBtns, resize_keyboard=False, one_time_keyboard=True
)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    name_greeting = message.from_user.first_name
    await message.answer(f"👋🏻")
    await asyncio.sleep(1.0)
    await message.answer(
        f"Long time no see, {name_greeting}! What would you like to do?",
        reply_markup=intro_reply,
    )


@dp.message_handler(Text(contains="🌍 New visited place"))
async def with_puree(message: types.Message):
    locationBtn = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    LocationBtn = types.KeyboardButton("📍 Share Location", request_location=True)
    locationBtn.add(LocationBtn)
    await message.answer("Wow! You decided to travel somewhere!")
    await message.answer(
        "Please, share your new location where you are now", reply_markup=locationBtn
    )


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def on_location(message: types.Message):
    location = message.location
    lat = str(location.latitude)
    lon = str(location.longitude)
    api_url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={openCageAPIkey}"
    print(api_url)
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            json_data = response.json()
            results = json_data.get("results", [])
            geodata = None
            for item in results:
                components = item.get("components", {})
                location_types = ["hamlet", "village", "town", "city"]
                for location_type in location_types:
                    if location_type in components:
                        geodata = [
                            components[location_type],
                            components["country"],
                            str(components["continent"]),
                            components["country_code"],
                            lat,
                            lon,
                        ]
                        country_code = components["country_code"].upper()
                        city_title = components[location_type]
                        continent = str(components["continent"])
                        map_color = ""
                        report_link = ""
                        short_text = ""
                        glyphtext = ""

                        if continent == "Europe":
                            map_color = "#FF0000"
                        elif continent == "Africa":
                            map_color = "#00FF00"
                        else:
                            map_color = "#192c55"


                        conn = psycopg2.connect(
                            dbname=bdName, user=bdUser, host=bdHost, password=bdPassword
                        )

                        # Create a cursor object
                        cur = conn.cursor()

                        query = "SELECT place_id FROM visited_places ORDER BY place_id DESC LIMIT 1;"
                        cur.execute(query)
                        current_id = cur.fetchone()[0]
                        place_id = current_id + 1

                        data = [
                            (
                                place_id,
                                country_code,
                                city_title,
                                map_color,
                                lat,
                                lon,
                                report_link,
                                short_text,
                                glyphtext
                            )
                        ]

                        for item in data:
                            cur.execute(
                                "INSERT INTO visited_places (place_id, country_code, city_title, color, lat, lon, report_link, short_text, glyphtext) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                item,
                            )
                        conn.commit()
                        cur.close()
                        conn.close()

                        await message.answer("Success! I've added your new place to the map! Would you like to add some notes about the place?")
                        break
            if geodata:
                print(geodata)
            else:
                print("Location not found.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    return geodata


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

