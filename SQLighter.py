import sqlite3


class SQLighter:

    def __init__(self, db_name):
        self._connection = sqlite3.connect(db_name)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def save(self, data):
        self._cursor.execute(f'insert into reminders (type, title, reminder_date) values {tuple(data)};')
        self._connection.commit()
