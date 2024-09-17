import sqlite3


class Database:
    def __init__(self, path_to_db="filmbot.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection  # Har safar yangi aloqani oching
        cursor = connection.cursor()
        data = None
        try:
            cursor.execute(sql, parameters)

            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

        return data

    # Create table
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname varchar(255) ,
            telegram_id varchar(20) NOT NULL UNIQUE, 
            language varchar(3)
            );
"""
        await self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int = None, fullname: str = None, telegram_id: str = None, language: str = 'uz'):
        sql = """
        INSERT INTO Users(id, fullname, telegram_id, language) 
        VALUES(?, ?, ?, ?)
        """
        await self.execute(sql, parameters=(id, fullname, telegram_id, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT telegram_id FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    async def count_users(self):

        return await self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_language(self, language, telegram_id):

        sql = f"""
        UPDATE Users SET language=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(language, telegram_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    async def create_table_films(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NULL,
            quality TEXT NULL,
            language TEXT NULL,
            resource TEXT NULL,
            file_id TEXT NOT NULL
        );
        """
        await self.execute(sql, commit=True)

    async def add_film(self, name, quality, language, resource, file_id):
        sql = """
        INSERT INTO Films (name, quality, language, resource, file_id) 
        VALUES (?, ?, ?, ?, ?)
        """
        await self.execute(sql, parameters=(name, quality, language, resource, file_id), commit=True)

        # Oxirgi kiritilgan id ni olish
        result = await self.execute("SELECT last_insert_rowid()", fetchone=True)
        return result[0] if result else None

    async def get_film_by_id(self, film_id):
        sql = "SELECT * FROM Films WHERE id=?"
        return await self.execute(sql, parameters=(film_id,), fetchone=True)

    # Create Channels Table
    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_username TEXT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, commit=True)

    # Kanal qo'shish
    async def add_channel(self, channel_username):
        sql = """
        INSERT INTO Channels (channel_username) 
        VALUES (?)
        """
        print(f"Kanal qo'shilmoqda: {channel_username}")

        try:
            await self.execute(sql, parameters=(channel_username,), commit=True)
        except sqlite3.IntegrityError:
            print(f"Channel {channel_username} already exists")

    # Kanallarni olish
    async def get_all_channels(self):
        sql = "SELECT channel_username FROM Channels"
        channels = await self.execute(sql, fetchall=True)
        print(f"Kanallar: {channels}")  # Kanallarni chop etish
        return channels

    # Kanalni o'chirish
    async def delete_channel(self, channel_username):
        sql = "DELETE FROM Channels WHERE channel_username = ?"
        await self.execute(sql, parameters=(channel_username,), commit=True)
