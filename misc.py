from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import *

help_text = """
Bот все команды:
/start - начало работы с ботом
/help - показ этого сообщения


"""

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Клавиатура для меня
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kbs = ReplyKeyboardMarkup(resize_keyboard=True)
kbn = ReplyKeyboardMarkup(resize_keyboard=True)
kbb = KeyboardButton('Назад‍')
kbn0 = KeyboardButton('👀К Новостям👀')
kbn1 = KeyboardButton('👀Все Новости👀')
kbn2 = KeyboardButton('👀Последние новости👀')
kbn3 = KeyboardButton('👀Последние пять новостей👀')
kbn.add(kbn1, kbn2, kbn3)
kb.add(KeyboardButton('💜Пожелать спокойной ночи пупсику💜'))
kb.add(KeyboardButton('👽Санёк👽'), kbn0)
kbs1 = KeyboardButton('🍺Пиво и Саня🍺')
kbs2 = KeyboardButton('🚬Сижки и Саня🚬')
kbn5 = KeyboardButton('👀Новости👀')
kbs.add(kbs1, kbs2, kbb)


# Клавиатура для всех
kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(KeyboardButton('/help'), kbn0)

# Клавиатура для Сани
kb3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb3.add(KeyboardButton('/no_sigi'))
kb3.add(KeyboardButton('/yes_sigi'))

ikb = InlineKeyboardMarkup(row_width=2)
ikb1 = InlineKeyboardButton(text='неа',
                            callback_data='no')
ikb2 = InlineKeyboardButton(text='YES YES YES',
                            callback_data='yes')
ikb.add(ikb1, ikb2)
