import aiosqlite


class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    async def add_user(self, user_id_telegram, firstname, username):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT OR IGNORE INTO users (user_id_telegram, firstname, username) VALUES (?, ?, ?)',
                             (user_id_telegram,
                              firstname,
                              username))
            await db.commit()

    async def update_discord_id(self, user_id_ds, user_id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET user_id_discord = ? WHERE user_id_telegram = ?',
                             (user_id_ds,
                              user_id_tg))
            await db.commit()

    async def full_info_user(self, user_id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users WHERE user_id_telegram = ?',
                                  (user_id_tg,)) as cursor:
                info = await cursor.fetchone()
                return info

    async def update_cooldown_tg(self, cooldown_tg, user_id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET cooldown_telegram = ? WHERE user_id_telegram = ?',
                             (cooldown_tg,
                              user_id_tg))
            await db.commit()

    async def info_cooldown_tg(self, user_id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT cooldown_telegram FROM users WHERE user_id_telegram = ?',
                                  (user_id_tg,)) as cursor:
                info_cooldown = await cursor.fetchone()
                return info_cooldown[0]

    async def info(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users') as cursor:
                users = await cursor.fetchall()
                return users

    async def update_cooldown_ds(self, cooldown, user_id_ds):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET cooldown_discord = ? WHERE user_id_discord = ?',
                             (cooldown, user_id_ds))
            await db.commit()

    async def info_cooldown_ds(self, user_id_ds):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT cooldown_discord FROM users WHERE user_id_discord = ?',
                                  (user_id_ds,)) as cursor:
                info_cooldown = await cursor.fetchone()
                return info_cooldown[0]

    async def info_id(self, name):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT user_id_telegram FROM users WHERE firstname = ?',
                                  (name,)) as cursor:
                info_id = await cursor.fetchone()
                return info_id[0]

    async def update_notif(self, notifications, user_id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET notifications = ? WHERE user_id_telegram = ?',
                             (notifications,
                              user_id_tg))
            await db.commit()

    async def info_id_not(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT user_id_telegram FROM users WHERE notifications = "Включены"') as cursor:
                result = await cursor.fetchall()
                return [row[0] for row in result]

    async def all_user_id_tg(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT user_id_telegram FROM users') as cursor:
                result = await cursor.fetchall()
                return [row[0] for row in result]

    async def update_counter_tg(self, counter_telegram, user_id_telegram):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET counter_telegram = ? WHERE user_id_telegram = ?',
                             (counter_telegram,
                              user_id_telegram))
            await db.commit()

    async def update_counter_ds(self, counter_discord, user_id_discord):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET counter_discord = ? WHERE user_id_discord = ?',
                             (counter_discord,
                              user_id_discord))
            await db.commit()

    async def info_counter_tg(self, user_id_telegram):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT counter_telegram FROM users WHERE user_id_telegram = ?',
                                  (user_id_telegram,)) as cursor:
                counter_tg = await cursor.fetchone()
                return counter_tg[0]

    async def info_counter_ds(self, user_id_discord):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT counter_discord FROM users WHERE user_id_discord = ?',
                                  (user_id_discord,)) as cursor:
                counter_ds = await cursor.fetchone()
                return counter_ds[0]
