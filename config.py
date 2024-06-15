from pymongo import MongoClient
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Клавиатура
kbn1 = KeyboardButton('👀Усі новини👀')
kbn2 = KeyboardButton('👀Останні новини👀')
kbn3 = KeyboardButton('👀Останні 5 новин👀')
kbn4 = KeyboardButton('👀Підписатися на розсилку👀')
kbn5 = KeyboardButton('👀Відписатися👀')
kbn = ReplyKeyboardMarkup(resize_keyboard=True).add(kbn1, kbn2, kbn3, kbn4, kbn5)

# Подключаем СУБД
cluster = MongoClient(os.getenv('MONGO_CLIENT'))
db = cluster["Users"]
collection = db["users"]


