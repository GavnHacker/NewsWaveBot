import asyncio
import json
from aiogram.utils.markdown import hlink
from aiogram import executor
from parser import check_update
from datetime import datetime
from config import *


async def on_startup(_):
    print('Миша работает')


@dp.message_handler(commands=['start'])
async def menu(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Слава Україні, Козаче!', reply_markup=kbn)
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEGr9xjjR49ti7T8kM2llVwrhta1ResGQACXBoAArwDyEvWLJR80o69LysE')

    await message.delete()


@dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message):
    uid = message.from_user.id
    name = message.from_user.full_name
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    if message.text == '👀Усі новини👀':
        for k, v in sorted(news_dict.items()):
            news = f'{hlink(v["title"], v["link"])}'

            await message.answer(news)
        await message.delete()

    elif message.text == '👀Останні 5 новин👀':
        for k, v in sorted(news_dict.items())[-5:]:
            news = f'{hlink(v["title"], v["link"])}'

            await message.answer(news)
        await message.delete()

    elif message.text == '👀Останні новини👀':
        if len(check_update()) >= 1:
            for k, v in sorted(check_update().items()):
                news = f'{hlink(v["title"], v["link"])}'

                await message.answer(news)

        else:
            await message.answer("Поки що немає свіжих новин")
        await message.delete()

    elif message.text == '👀Підписатися на розсилку👀':
        try:
            collection.insert_one({
                "_id": uid,
                "name": name
            })
            await bot.send_message(message.from_user.id, text='Ви успішно підписалися')
        except:
            await bot.send_message(message.from_user.id, text="Ви вже підписані")
        await message.delete()

    elif message.text == '👀Відписатися👀':
        try:
            collection.delete_one({'_id': uid})
            await bot.send_message(message.from_user.id, text='Ви успішно відписалися')
        except:
            await bot.send_message(message.from_user.id, text='Ви ще не підписані')
        await message.delete()


async def news_every_minute(wait):
    users = collection.find()
    while True:
        fresh_news = check_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f'{hlink(v["title"], v["link"])}'
                for user in users:
                    uid = user["_id"]
                    await bot.send_message(uid, news, disable_notification=True)
                print(news)
        fresh_news.clear()
        print(datetime.now())
        await asyncio.sleep(wait)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute(30))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
