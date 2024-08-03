import asyncio
from aiogram import Bot, Dispatcher, types
from disnake.ext import commands

# Настройки для ботов
TELEGRAM_TOKEN = '7498090524:AAHp2tQbpRDtUEJEVeqxaMSpwJLr9A4EzsQ'
DISCORD_TOKEN = 'MTI2OTIxNTk1Mjc0MzA0MzA3Mg.GkS8Gp.f4tqsFp6kelm8YVSFNmfQnrj4_1nvSU4Yfshq4'
DISCORD_CHANNEL_ID = 1269214873045307516  # ID канала в Discord

# Инициализация ботов
telegram_bot = Bot(token=TELEGRAM_TOKEN)
telegram_dp = Dispatcher(telegram_bot)

discord_bot = commands.Bot(command_prefix='!')


@telegram_dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_telegram_message(message: types.Message):
    print(f"Received message from Telegram: {message.text}")  # Отладочное сообщение
    text = message.text
    discord_channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)
    if discord_channel:
        await discord_channel.send(text)
        print("Message sent to Discord")  # Отладочное сообщение
    else:
        print("Discord channel not found")  # Отладочное сообщение


@discord_bot.event
async def on_ready():
    print(f'Logged in as {discord_bot.user}!')


async def start_bots():
    # Запускаем оба бота
    await asyncio.gather(
        telegram_dp.start_polling(),
        discord_bot.start(DISCORD_TOKEN)
    )

async def main():
    try:
        await discord_bot.start(DISCORD_TOKEN)  # Здесь мы ожидаем старта Discord бота
        await start_bots()
    finally:
        await telegram_bot.session.close()
        await discord_bot.close()

if __name__ == '__main__':
    asyncio.run(main())