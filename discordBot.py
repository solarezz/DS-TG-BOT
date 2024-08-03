import disnake
import asyncio
#from telegramBot import *
from disnake.ext import commands
from database import Database
from art import *
from aiogram import Bot, Dispatcher, types

token = 'MTI2OTIxNTk1Mjc0MzA0MzA3Mg.GkS8Gp.f4tqsFp6kelm8YVSFNmfQnrj4_1nvSU4Yfshq4'
TELEGRAM_TOKEN = '7498090524:AAHp2tQbpRDtUEJEVeqxaMSpwJLr9A4EzsQ'

intents = disnake.Intents.default().all()
intents.messages = True
intents.guilds = True
intents.message_content = True

db = Database()

telegram_bot = Bot(token=TELEGRAM_TOKEN)
telegram_dp = Dispatcher(telegram_bot)
bot = commands.Bot(command_prefix='/', intents=intents)



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(name='info', description="Информация зарегистрированных пользователей в телеграмм")
async def info(interaction: disnake.ApplicationCommandInteraction):
    users = await db.info()
    user_list = '\n'.join([f'{user[0]} - {user[1]}' for user in users])
    embed = disnake.Embed(title=f'Пользователи которым вы можете отправить сообщение:\n', color=0x00ff00)
    embed.add_field(name='ID в Телеграмм - Имя в Телеграмм', value=user_list)
    await interaction.send(embed=embed, ephemeral=True)
    channel = bot.get_channel(1269214873045307516)
    await channel.send("rewrite")
    for guild in bot.guilds:
        print(f'Сервер: {guild.name} (ID: {guild.id})')
        for channel in guild.channels:
            print(f'Канал: {channel.name} (ID: {channel.id}, Тип: {channel.type})')


@bot.slash_command(name='send_tg', description="Отправить сообщение в телеграмм")
async def send_tg(interaction: disnake.ApplicationCommandInteraction, user_id, message: str):
    user = interaction.user
    info = await db.info_user(user_id)
    await interaction.send(f"Вы отправили сообщение пользователю - {info[0]}!")
    await telegram_bot.send_message(user_id, f'[{message}] - от {user.name}')


#@bottg.message_handler(content_types=types.ContentTypes.TEXT)
async def send_in_discord(message: types.Message):
    embed = disnake.Embed(title=f"Сообщение из телеграмм от {message.from_user.first_name}", color=0x5da6e8)
    embed.add_field(name='Содержание сообщение:', value=message.text)
    channel = bot.get_channel(1269214873045307516)
    await channel.send(embed=embed)

async def main():
    # Запускаем оба бота
    await asyncio.gather(telegram_dp.start_polling(), bot.run(token))

print(text2art("BOT STARTED"))
if __name__ == '__main__':
    asyncio.run(main())
