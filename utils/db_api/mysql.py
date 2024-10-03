import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @property
    def connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor(dictionary=True)
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()

        cursor.close()
        connection.close()
        return data

    def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def create_table_channel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS channel (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id INT NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def create_table_data(self):
        sql = """
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name TEXT NOT NULL,
            file_id TEXT NOT NULL,
            kod TEXT NOT NULL,
            `all` TEXT NOT NULL
        ) COLLATE = utf8mb4_general_ci;
        """
        self.execute(sql, commit=True)

    def create_table_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS `groups` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id VARCHAR(64) NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def create_table_kanal(self):
        sql = """
        CREATE TABLE IF NOT EXISTS kanal (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id VARCHAR(64) NOT NULL,
            url TEXT NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def create_table_sendusers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS sendusers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mid INT NOT NULL,
            soni INT NOT NULL,
            boshlash_vaqt VARCHAR(50) NOT NULL,
            joriy_vaqt VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            send VARCHAR(50) NOT NULL,
            holat VARCHAR(50) NOT NULL,
            nosend VARCHAR(250) NOT NULL,
            qayerga TEXT NOT NULL,
            admin TEXT NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL,
            ban INT NOT NULL,
            sana TEXT NOT NULL,
            status TEXT NOT NULL
        ) CHARSET = utf8mb3;
        """
        self.execute(sql, commit=True)

    def add_admin(self, user_id: str):
        sql = """
        INSERT INTO admins(user_id) VALUES (%s)
        """
        self.execute(sql, parameters=(user_id,), commit=True)

    def add_channel(self, chat_id: int):
        sql = """
        INSERT INTO channel(chat_id) VALUES (%s)
        """
        self.execute(sql, parameters=(chat_id,), commit=True)

    def add_data(self, file_name: str, file_id: str, kod: str, all_data: str):
        sql = """
        INSERT INTO data(file_name, file_id, kod, `all`) VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, parameters=(file_name, file_id, kod, all_data), commit=True)

    def add_group(self, chat_id: str):
        sql = """
        INSERT INTO `groups`(chat_id) VALUES (%s)
        """
        self.execute(sql, parameters=(chat_id,), commit=True)

    def add_kanal(self, chat_id: str, url: str):
        sql = """
        INSERT INTO kanal(chat_id, url) VALUES (%s, %s)
        """
        self.execute(sql, parameters=(chat_id, url), commit=True)

    def delete_kanal(self, chat_id):
        sql = "DELETE FROM kanal WHERE chat_id = %s"
        self.execute(sql, parameters=(chat_id,), commit=True)

    def get_all_url(self):
        sql = "SELECT url FROM kanal"
        channels = self.execute(sql, fetchall=True)
        return [channel['url'] for channel in channels]  # Faqat url'ni qaytaradi


    def add_senduser(self, mid: int, soni: int, boshlash_vaqt: str, joriy_vaqt: str, status: str, send: str, holat: str,
                     nosend: str, qayerga: str, admin: str):
        sql = """
        INSERT INTO sendusers(mid, soni, boshlash_vaqt, joriy_vaqt, status, send, holat, nosend, qayerga, admin) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute(sql,
                     parameters=(mid, soni, boshlash_vaqt, joriy_vaqt, status, send, holat, nosend, qayerga, admin),
                     commit=True)

    def add_user(self, user_id: str, ban: int, sana: str, status: str):
        sql = """
        INSERT INTO users(user_id, ban, sana, status) VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, parameters=(user_id, ban, sana, status), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def get_all_channels(self):
        sql = """
        SELECT * FROM kanal
        """
        return self.execute(sql, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(user_id) as total FROM users;", fetchone=True)


    def delete_all_users(self):
        sql = """
        DELETE FROM users WHERE TRUE
        """
        self.execute(sql, commit=True)

    def get_film_by_id(self, data_id: int):
        sql = """
        SELECT * FROM data WHERE kod = %s
        """
        return self.execute(sql, parameters=(data_id,), fetchone=True)

    def get_user(self, user_id: int):
        sql = """
        SELECT * FROM users WHERE user_id = %s
        """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def add_film_data(self, file_name: str, file_id: str, kod: str, all_data: str):
        sql = """
        INSERT INTO data(file_name, file_id, kod, `all`) VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, parameters=(file_name, file_id, kod, all_data), commit=True)

    def get_all_data(self):
        sql = """
        SELECT * FROM data
        """
        return self.execute(sql, fetchall=True)

    def check_code_exists(self, kod):
        query = "SELECT EXISTS(SELECT 1 FROM data WHERE kod = %s)"
        result = self.execute(query, parameters=(kod,), fetchone=True)

        # Natija faqat bitta qiymatni qaytaradi ('EXISTS' natijasi), shuning uchun biz faqat birinchi qiymatni olamiz
        return list(result.values())[0]

    def delete_film_id(self, kod):
        sql = """
        DELETE FROM data WHERE kod = %s"""
        return self.execute(sql, parameters=(kod,), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")