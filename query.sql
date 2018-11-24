CREATE TABLE reminders (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    reminder_date datetime  NOT NULL
    );
