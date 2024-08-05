import disnake
import asyncio
import logging
from disnake.ext import commands
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database
from aiogram import Bot, Dispatcher, types

token = ''

intents = disnake.Intents.default().all()

db = Database()

ID_CHANNEL = 875772759806984234

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''

bottg = Bot(token=API_TOKEN)
dp = Dispatcher(bottg, storage=MemoryStorage())

bot = commands.Bot(command_prefix='/', intents=intents)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bottg.send_message(message.chat.id, "[✅] Вы успешно внесли свои данные в бота!")
    await db.add_user(user_id=message.chat.id, name=message.from_user.first_name)


@dp.message_handler()
async def message_in_discord(message: types.Message):
    cooldown = 15
    info_cd = await db.info_cooldown_tg(user_id=message.chat.id)
    if info_cd == 0:
        user_text = message.text
        await on_ready(name=message.from_user.first_name, message=user_text)
        await db.update_cooldown_tg(cooldown=cooldown, user_id=message.chat.id)
        asyncio.create_task(handle_cooldown_tg(message.chat.id, cooldown))
    else:
        await message.answer(f"[❌] Вы сможете отправлять команды через {info_cd} секунд!")

async def handle_cooldown_tg(user_id, cooldown):
    while cooldown > 0:
        await asyncio.sleep(1)  # Ждем 1 секунду
        cooldown -= 1
        await db.update_cooldown_tg(cooldown=cooldown, user_id=user_id)
    await bottg.send_message(user_id, "[✅] Вы вновь можете отправлять сообщения в дискорд!")

@bot.event
async def on_ready(name, message):
    try:
        embed = disnake.Embed(title=f"[📩] Сообщение из телеграмм от {name}", color=0x5da6e8)
        embed.add_field(name='[📝] Содержание сообщение:', value=message)
        channel = bot.get_channel(ID_CHANNEL)
        await channel.send(embed=embed)
    except TypeError:
        print(f'We have logged in as {bot.user}')


@bot.slash_command(name='info', description="Информация зарегистрированных пользователей в телеграмм")
async def info(interaction: disnake.ApplicationCommandInteraction):
    users = await db.info()
    user_list = '\n'.join([f'{user[0]} - {user[1]}' for user in users])
    embed = disnake.Embed(title=f'[🌐] Пользователи которым вы можете отправить сообщение:\n', color=0x00ff00)
    embed.add_field(name='[🆔] ID в Телеграмм - [🟣] Имя в Телеграмм', value=user_list)
    await interaction.send(embed=embed, ephemeral=True)
    check = await db.info_cooldown_ds(user_id_ds=interaction.author.id)


@bot.slash_command(name='send_tg', description="Отправить сообщение в телеграмм")
async def send_tg(interaction: disnake.ApplicationCommandInteraction, user_id, message: str):
    cooldown = 15
    info_cd = await db.info_cooldown_ds(user_id_ds=interaction.author.id)
    if info_cd == 0:
        user = interaction.user
        user_info = await db.info_user(user_id)
        await interaction.send(f"[📨] Вы отправили сообщение пользователю - {user_info[0]}!")
        await bottg.send_message(user_id, f'[{message}] - от {user.name}')
        await db.update_cooldown_ds(cooldown=cooldown, user_id_ds=interaction.author.id)
        asyncio.create_task(handle_cooldown(interaction.author.id, cooldown))
    else:
        await interaction.send(f"[❌] Вы сможете отправлять команды через {info_cd} секунд!")

async def handle_cooldown(user_id_ds, cooldown):
    while cooldown > 0:
        await asyncio.sleep(1)  # Ждем 1 секунду
        cooldown -= 1
        await db.update_cooldown_ds(cooldown=cooldown, user_id_ds=user_id_ds)
    user = bot.get_user(user_id_ds)
    await user.send("[✅] Вы вновь можете отправлять сообщения в телеграмм!")

@bot.slash_command(name="dev", description="Разработчик бота")
async def dev(interaction: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(title="[👨🏻‍💻] О боте:", color=0x185200)
    embed.add_field(name="[🛠] Разработчик", value="@solarezzwhynot")
    embed.add_field(name="[⚙️] Версия", value="0.3")
    embed.add_field(name="[💳] Поддержка копеечкой для хостинга", value="2200 7007 1699 4750")
    await interaction.send(embed=embed)


async def main():
    # Start the Telegram bot
    await dp.start_polling()


# Run both bots
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_until_complete(bot.start(token))
