import disnake
import asyncio
import logging
from disnake.ext import commands
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database
from aiogram import Bot, Dispatcher, types

token = 'MTI2OTIxNTk1Mjc0MzA0MzA3Mg.GkS8Gp.f4tqsFp6kelm8YVSFNmfQnrj4_1nvSU4Yfshq4'

intents = disnake.Intents.default().all()


db = Database()

ID_CHANNEL = 1269214873045307516

logging.basicConfig(level=logging.INFO)

API_TOKEN = '7498090524:AAHp2tQbpRDtUEJEVeqxaMSpwJLr9A4EzsQ'

bottg = Bot(token=API_TOKEN)
dp = Dispatcher(bottg, storage=MemoryStorage())

bot = commands.Bot(command_prefix='/', intents=intents)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bottg.send_message(message.chat.id, "Вы успешно внесли свои данные в бота!")
    await db.add_user(user_id=message.chat.id, name=message.from_user.first_name)

@dp.message_handler()
async def message_in_discord(message: types.Message):
    user_text = message.text
    await on_ready(name=message.from_user.first_name, message=user_text)


@bot.event
async def on_ready(name, message):
    try:
        embed = disnake.Embed(title=f"Сообщение из телеграмм от {name}", color=0x5da6e8)
        embed.add_field(name='Содержание сообщение:', value=message)
        channel = bot.get_channel(ID_CHANNEL)
        await channel.send(embed=embed)
    except TypeError:
        print(f'We have logged in as {bot.user}')




@bot.slash_command(name='info', description="Информация зарегистрированных пользователей в телеграмм")
async def info(interaction: disnake.ApplicationCommandInteraction):
    users = await db.info()
    user_list = '\n'.join([f'{user[0]} - {user[1]}' for user in users])
    embed = disnake.Embed(title=f'Пользователи которым вы можете отправить сообщение:\n', color=0x00ff00)
    embed.add_field(name='ID в Телеграмм - Имя в Телеграмм', value=user_list)
    await interaction.send(embed=embed, ephemeral=True)


@bot.slash_command(name='send_tg', description="Отправить сообщение в телеграмм")
async def send_tg(interaction: disnake.ApplicationCommandInteraction, user_id, message: str):
    user = interaction.user
    user_info = await db.info_user(user_id)
    await interaction.send(f"Вы отправили сообщение пользователю - {user_info[0]}!")
    await bottg.send_message(user_id, f'[{message}] - от {user.name}')


async def main():
    # Start the Telegram bot
    await dp.start_polling()


# Run both bots
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_until_complete(bot.start(token))
