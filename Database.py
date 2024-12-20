import sqlite3


# Класс для работы с базой данных
class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Удаляем существующие таблицы, если они есть
        self.cursor.execute('DROP TABLE IF EXISTS reviews')
        self.cursor.execute('DROP TABLE IF EXISTS aggregate_ratings')

        # Создаем таблицы
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS aggregate_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating_value REAL,
            review_count INTEGER,
            best_rating REAL,
            worst_rating REAL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            date_published TEXT,
            description TEXT,
            name TEXT,
            rating_value REAL,
            aggregate_rating_id INTEGER,
            FOREIGN KEY (aggregate_rating_id) REFERENCES aggregate_ratings (id)
        )
        ''')
        self.conn.commit()

    def save_aggregate_rating(self, rating_value, review_count, best_rating, worst_rating):
        self.cursor.execute('''
        INSERT INTO aggregate_ratings (rating_value, review_count, best_rating, worst_rating)
        VALUES (?, ?, ?, ?)
        ''', (rating_value, review_count, best_rating, worst_rating))
        self.conn.commit()
        return self.cursor.lastrowid  # Возвращаем ID вставленной записи

    def save_review(self, author, date_published, description, name, rating_value, aggregate_rating_id):
        self.cursor.execute('''
        INSERT INTO reviews (author, date_published, description, name, rating_value, aggregate_rating_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (author, date_published, description, name, rating_value, aggregate_rating_id))
        self.conn.commit()

    def close(self):
        self.conn.close()