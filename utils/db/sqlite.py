import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            hemis_id int NOT NULL,
            password varchar(25) NOT NULL,
            user_id int NOT NULL,
            name varchar(255),
            department text,
            staff_position text,
            phone_num varchar(25),
            language varchar(3),
            PRIMARY KEY (hemis_id)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, hemis_id: int,
                 password: str, 
                 user_id: int, 
                 name: str = None, 
                 department: str = None, 
                 staff_position: str = None,
                 phone_num: str = None,  
                 language: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users( hemis_id, password, user_id, name,department, staff_position, phone_num, language ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(hemis_id, password, user_id,name, department, staff_position, phone_num, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    
        
    def check_user_password(self, hemis_id, password):
        sql = '''SELECT EXISTS (
                SELECT 1
                FROM Users
                WHERE hemis_id = ? AND password = ?
            )'''
        return self.execute(sql, parameters=(hemis_id, password), fetchone=True)
    
    def check_user_exists(self, hemis_id):
        sql = '''SELECT EXISTS (
                SELECT 1
                FROM Users
                WHERE hemis_id = ?
            )'''
        return self.execute(sql, parameters=(hemis_id), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_password(self, hemis_id, password):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET password=? WHERE hemis_id=?
        """
        self.execute(sql, parameters=(password, hemis_id), commit=True)
    
    def update_user_phone(self, hemis_id, phone_num):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone_num=? WHERE hemis_id=?
        """
        self.execute(sql, parameters=(phone_num, hemis_id), commit=True)
    
    def update_user_lang(self, language, user_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET language=? WHERE user_id=?
        """
        self.execute(sql, parameters=(language, user_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
