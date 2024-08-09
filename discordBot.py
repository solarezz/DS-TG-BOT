import disnake
import asyncio
import logging
from aiogram.dispatcher.filters.state import StatesGroup, State
from disnake.ext import commands
from database import Database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


ds_token = ''

tg_token = ''

intents = disnake.Intents.default().all()

db = Database()

ID_CHANNEL = 1059414521422290988

logging.basicConfig(level=logging.INFO)

tg = Bot(token=tg_token)
dp = Dispatcher(tg, storage=MemoryStorage())

ds = commands.Bot(command_prefix='/', intents=intents)


class Form(StatesGroup):
    waiting_for_discord_id = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    info = await db.full_info_user(message.chat.id)
    if not info:
        kb = [
            [
                types.KeyboardButton(text="👔 Привязать дискорд")
            ]
        ]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        await tg.send_message(message.chat.id, "[✅] Вы успешно внесли свои данные в бота!", reply_markup=markup)
        await db.add_user(user_id_telegram=message.chat.id,
                          firstname=message.from_user.first_name,
                          username=message.from_user.username)
    elif not info[1]:
        kb = [
            [
                types.KeyboardButton(text="👔 Привязать дискорд")
            ]
        ]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        await tg.send_message(message.chat.id, "[✍] Привяжите свой дискорд!", reply_markup=markup)
    else:
        await tg.send_message(message.chat.id, '[👌] Вы уже зарегистрированы!')

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.id == 2023527964:
        message_options = message.text
        list = await db.all_user_id_tg()
        kb = [
            [
                types.KeyboardButton(text="/notifications")
            ]
        ]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        for user in list:
            await tg.send_message(user, f'{message_options[0]}', reply_markup=markup)

        await tg.send_message(message.chat.id, f'отправили всем [{list}]')
    else:
        pass

@dp.message_handler(commands=['notifications'])
async def notifications(message: types.Message):
    check_not = await db.full_info_user(message.chat.id)
    if check_not[6] == "Выключены":
        await db.update_notif(notifications="Включены", user_id_tg=message.chat.id)
        await tg.send_message(message.chat.id, "[🟢] Вы включили уведомления с дискорда!")
    elif check_not[6] == 'Включены':
        await db.update_notif(notifications="Выключены", user_id_tg=message.chat.id)
        await tg.send_message(message.chat.id, "[🔴] Вы выключили уведомления с дискорда!")
    else:
        await tg.send_message("[⛔] Вы не зарегистрированы. Напишите /start для регистрации!")

@dp.message_handler(lambda msg: msg.text.startswith('👔 Привязать дискорд'))
async def input_id_discord(message: types.Message):
    await Form.waiting_for_discord_id.set()
    await message.answer("Что бы узнать свой Discord ID, введите в Discord команду /myid")
    await message.reply('Пожалуйста введите свой Discord ID:')


@dp.message_handler(commands=['discord'])
async def input_id_discord(message: types.Message):
    await Form.waiting_for_discord_id.set()
    await message.answer("Что бы узнать свой Discord ID, введите в Discord команду /myid")
    await message.reply('Пожалуйста введите свой Discord ID:')


@dp.message_handler(state=Form.waiting_for_discord_id)
async def process_discord_id(message: types.Message, state: FSMContext):
    discord_id = message.text
    try:
        discord_int = int(discord_id)
        await db.update_discord_id(user_id_tg=message.chat.id,
                                   user_id_ds=discord_id)
        types.ReplyKeyboardRemove()
        kb = [
            [
                types.KeyboardButton(text="/notifications")
            ]
        ]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        await message.reply(
            f"Ваш Discord ID {discord_id} успешно привязан!\nЕсли вдруг вы случайно ввели не тот ID, напишите команду /discord", reply_markup=markup)
        await state.finish()
    except ValueError:
        await message.reply("Пожалуйста, введите корректный Discord ID (число).")


@dp.message_handler()
async def message_in_discord(message: types.Message):
    cooldown = 15
    info_cd = await db.info_cooldown_tg(user_id_tg=message.chat.id)
    if info_cd == 0:
        user_text = message.text
        await on_ready(name=message.from_user.first_name, message=user_text)
        await db.update_cooldown_tg(cooldown_tg=cooldown, user_id_tg=message.chat.id)
        asyncio.create_task(handle_cooldown_tg(message.chat.id, cooldown))
    else:
        await message.answer(f"[❌] Вы сможете отправлять команды через {info_cd} секунд!")


async def handle_cooldown_tg(user_id, cooldown):
    while cooldown > 0:
        await asyncio.sleep(1)  # Ждем 1 секунду
        cooldown -= 1
        await db.update_cooldown_tg(cooldown_tg=cooldown, user_id_tg=user_id)
    await tg.send_message(user_id, "[✅] Вы вновь можете отправлять сообщения в дискорд!")


@ds.event
async def on_ready(name, message):
    URL = f'[{name}](https://t.me/{name})'
    embed = disnake.Embed(title=f"[📩] Сообщение из телеграмм от: ", description=URL, color=disnake.Colour.blue())
    embed.add_field(name='[📝] Содержание сообщение:', value=message)
    embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/round-set-vol-2/120/sending-1024.png")
    channel = ds.get_channel(ID_CHANNEL)
    await channel.send(embed=embed)


@ds.event
async def on_message(message):
    if message.author == ds.user:
        return

    user_list = await db.info_id_not()

    for userid in user_list:
        await tg.send_message(userid, f'{message.author}:\n{message.content}')

@ds.slash_command(name="myid", description='Информация о ID пользователя')
async def myid(interaction: disnake.ApplicationCommandInteraction):
    await interaction.send(f'Ваш ID: {interaction.author.id}', ephemeral=True)


@ds.slash_command(name='info', description="Информация зарегистрированных пользователей в телеграмм")
async def info(interaction: disnake.ApplicationCommandInteraction):
    users = await db.info()
    user_list = '\n'.join([f'{user[2]} - @{user[3]}' for user in users])
    embed = disnake.Embed(title=f'[🌐] Пользователи которым вы можете отправить сообщение:\n',
                          color=disnake.Colour.blurple())
    embed.add_field(name='', value=user_list)
    embed.add_field(name="Как отправить сообщение?",
                    value="Ввести команду /stg -> выбрать кому отправить -> написать сообщение",
                    inline=False)
    embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/round-set-vol-2/120/sending-1024.png")
    await interaction.send(embed=embed, ephemeral=True)


@ds.slash_command(name='stg', description="Отправить сообщение в телеграмм")
async def stg(interaction: disnake.ApplicationCommandInteraction, name: str, message: str):
    try:
        cooldown = 15
        info_cd = await db.info_cooldown_ds(user_id_ds=interaction.author.id)
        if info_cd == 0:
            users = await db.info()
            user_list = [f'{user[2]}' for user in users]
            if name in user_list:
                user = interaction.user
                user_id = await db.info_id(name)
                await interaction.send(f"[📨] Вы отправили сообщение пользователю - {name}!")
                await tg.send_message(user_id, f'[{message}] - от {user.name}')
                await db.update_cooldown_ds(cooldown=cooldown, user_id_ds=interaction.author.id)
                asyncio.create_task(handle_cooldown(interaction.author.id, cooldown))
            else:
                await interaction.send(f"[❌] Вы выбрали не существующего человека!")
        else:
            await interaction.send(f"[❌] Вы сможете отправлять команды через {info_cd} секунд!")
    except:
        await interaction.send("[❌] Вы не привязали Discord ID к Telegram боту!")


@stg.autocomplete('name')
async def name_autocomplete(interaction: disnake.ApplicationCommandInteraction, current: str):
    users = await db.info()
    user_list = [f'{user[2]}' for user in users]
    choices = [name for name in user_list if current.lower() in name.lower()]
    return choices


async def handle_cooldown(user_id_ds, cooldown):
    while cooldown > 0:
        await asyncio.sleep(1)
        cooldown -= 1
        await db.update_cooldown_ds(cooldown=cooldown, user_id_ds=user_id_ds)
    user = ds.get_user(user_id_ds)
    await user.send("[✅] Вы вновь можете отправлять сообщения в телеграмм!")


@ds.slash_command(name="dev", description="Разработчик бота")
async def dev(interaction: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(title="[👨🏻‍💻] О боте:", color=0x185200)
    embed.add_field(name="[🛠] Разработчик", value="@solarezzwhynot")
    embed.add_field(name="[⚙️] Версия", value="0.6")
    embed.add_field(name="[💳] Поддержка копеечкой для хостинга", value="2200 7007 1699 4750")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/f8/d0/bc/f8d0bc025046ab637a78a09598b905a7.png")
    await interaction.send(embed=embed)


async def main():
    # Start the Telegram bot
    await dp.start_polling()


# Run both bots
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_until_complete(ds.start(ds_token))
