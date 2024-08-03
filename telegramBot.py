import logging

from database import Database
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
API_TOKEN = '7498090524:AAHp2tQbpRDtUEJEVeqxaMSpwJLr9A4EzsQ'

bottg = Bot(token=API_TOKEN)
dp = Dispatcher(bottg)

db = Database()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bottg.send_message(message.chat.id, "Вы успешно внесли свои данные в бота!")
    await db.add_user(user_id=message.chat.id, name=message.from_user.first_name)

@dp.message_handler()
async def message_in_discord(message: types.Message):
    from discordBot import send_in_discord
    user_text = message.text
    await send_in_discord(message=user_text, name=message.from_user.first_name)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
