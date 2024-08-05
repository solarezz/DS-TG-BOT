import aiosqlite


class Database:
    def __init__(self, db_name=r'C:\Users\solarezz\Desktop\database.db'):
        self.db_name = db_name

    async def add_user(self, user_id, name):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
            await db.commit()

    async def info(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users') as cursor:
                users = await cursor.fetchall()
                return users

    async def info_user(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)) as cursor:
                info_user = await cursor.fetchone()
                return info_user

    async def update_cooldown_ds(self, cooldown, user_id_ds):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET cooldown = ? WHERE user_id_ds = ?', (cooldown, user_id_ds))
            await db.commit()

    async def info_cooldown_ds(self, user_id_ds):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT cooldown FROM users WHERE user_id_ds = ?', (user_id_ds,)) as cursor:
                info_cooldown = await cursor.fetchone()
                return info_cooldown[0]

    async def update_cooldown_tg(self, cooldown, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET cooldown_tg = ? WHERE user_id = ?', (cooldown, user_id))
            await db.commit()

    async def info_cooldown_tg(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT cooldown_tg FROM users WHERE user_id = ?', (user_id,)) as cursor:
                info_cooldown = await cursor.fetchone()
                return info_cooldown[0]
