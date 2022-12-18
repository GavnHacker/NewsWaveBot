# from aiogram import Bot, executor, Dispatcher, types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# from config import *
import asyncio
import json

from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from misc import *
from parser import check_update
from datetime import datetime
import sqlite3

con = sqlite3.connect('ids.db')
cur = con.cursor()


def db_table_val(user_id: int, user_name: str, username: str):
	cur.execute('INSERT INTO users (user_id, user_name, username) VALUES (?, ?, ?, ?)', (user_id, user_name, username))
	con.commit()


async def on_startup(_):
    print('Миша работает')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.from_user.id == ADMIN:
        await bot.send_message(chat_id=message.from_user.id, text='Здравствуйте хозяин', reply_markup=kb)
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker='CAACAgIAAxkBAAEGr9xjjR49ti7T8kM2llVwrhta1ResGQACXBoAArwDyEvWLJR80o69LysE')
    elif message.from_user.id == sanya_id:
        await bot.send_message(chat_id=message.from_user.id, text='Привет Санёк', reply_markup=kb3)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Привет, я Мишаня)",
                               reply_markup=kb2)
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEGrv1jjOcThne6GhikgH2Xo_U3clV5SQACFwAD6QViAAF8VoBtPZmBrysE")
        # await bot.send_message(ADMIN, text=[message.from_user.id, message.from_user.username, message.from_user.full_name])
        await message.delete()


@dp.message_handler(Text(equals='👀К Новостям👀'))
async def to_news(message: types.Message):
    await message.answer(text='Какие новости интересны?', reply_markup=kbn)


@dp.message_handler(Text(equals='👀Все Новости👀'))
async def all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items()):
        news = f'{hlink(v["title"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='👀Последние пять новостей👀'))
async def last_five(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items())[-5:]:
        news = f'{hlink(v["title"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='👀Последние новости👀'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f'{hlink(v["title"], v["link"])}'

            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей")


@dp.message_handler(Text(equals='👽Санёк👽'))
async def sanya(message: types.Message):
    if message.from_user.id == ADMIN:
        await bot.send_message(ADMIN, text=f'Шо мы от него хотим, {message.from_user.full_name}?', reply_markup=kbs)

    await message.delete()


@dp.message_handler(Text(equals='Назад'))
async def back(message: types.Message):
    await message.answer(text='Добро пожаловать в главное меню', reply_markup=kb)
    await message.delete()


@dp.message_handler(Text(equals='🍺Пиво и Саня🍺'))
async def pivo_command(message: types.Message):
    if message.from_user.id == ADMIN:
        await bot.send_photo(sanya_id,
                             photo='https://fastly.4sqi.net/img/general/600x600/72187219_Jnw_sN9luzEobypWQw_sREu6iWvWNlPRjM5vaE2_6EY.jpg',
                             caption='Ебанём сегодня?',
                             reply_markup=ikb)
        await bot.send_message(ADMIN, text='Мы спросили ебанёт ли он с нами', reply_markup=kb)
    await message.delete()


@dp.message_handler(Text(equals='🚬Сижки и Саня🚬'))
async def sigi_command(message: types.Message):
    if message.from_user.id == ADMIN:
        await bot.send_photo(sanya_id,
                             photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWCa8jXEk906r-0Pn_wwFUb7W4uR2SuGi5jg&usqp=CAU',
                             caption='У тебя есть сиги?',
                             reply_markup=ikb)
        await bot.send_message(ADMIN, text='Мы спросили шо там Саня', reply_markup=kb)
    else:
        await message.answer(text='У вас недостаточно прав')
    await message.delete()


@dp.callback_query_handler()
async def sanya_callback(callback: types.CallbackQuery):
    if callback.data == 'no':
        await callback.answer(text='Ты пацюк')
        await bot.send_sticker(ADMIN,
                               sticker='CAACAgIAAxkBAAEGr95jjSLH8mB5CaWrCpyaWYS6bdmt8wACWUAAAuCjggc35LUFXNY5gCsE')
    elif callback.data == 'yes':
        await callback.answer(text='Люблю тебя')
        await bot.send_sticker(ADMIN,
                               sticker='CAACAgIAAxkBAAEGr-BjjSM3l5tIKqCQiZXKXrRTbBavAgACrwIAAiz8ww529QrQNyAinisE')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=help_text, parse_mode='HTML')
    await message.delete()


# @dp.message_handler(commands=['currency'])
# async def currency_command(message: types.Message):
#     await message.answer(text=data['rates']['UAH'])
#     await message.delete()


@dp.message_handler(Text(equals='👀Подписаться на рассылку👀'))
async def subscription(message: types.Message):
    uid = message.from_user.id
    user_id.append(uid)




async def news_every_minute(wait):
    while True:
        fresh_news = check_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f'{hlink(v["title"], v["link"])}'
                for id in users:
                    await bot.send_message(id, news, disable_notification=True)
                print(news)
        fresh_news.clear()
        print(datetime.now())
        await asyncio.sleep(wait)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute(20))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
