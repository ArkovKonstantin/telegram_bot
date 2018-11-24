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

    def get_reminders(self):
        self._cursor.execute('select reminder_date, type, title  from reminders order by reminder_date;')
        text = '\n'.join([' '.join(map(str, reminder)) for reminder in self._cursor.fetchall()])

        return text
