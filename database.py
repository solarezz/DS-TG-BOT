import aiosqlite

class Database:
    def __init__(self, db_name='database.db'):
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

