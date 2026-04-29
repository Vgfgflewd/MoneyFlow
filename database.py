import sqlite3
import datetime


class FinanceDB:
    def __init__(self):
        self.conn = sqlite3.connect("myDatabase.db")
        self.cursor = self.conn.cursor()
        self.tablic()

    def tablic(self):
        sql1 = "CREATE TABLE IF NOT EXISTS kategorii (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)"
        self.cursor.execute(sql1)

        sql2 = "CREATE TABLE IF NOT EXISTS rashodi (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL NOT NULL, cat_id INTEGER NOT NULL, date TEXT NOT NULL, FOREIGN KEY (cat_id) REFERENCES kategorii (id))"
        self.cursor.execute(sql2)

        self.cursor.execute("SELECT COUNT(*) FROM kategorii")
        if self.cursor.fetchone()[0] == 0:
            spisok = [("Еда",), ("Транспорт",), ("Развлечения",), ("Прочее",)]
            for item in spisok:
                self.cursor.execute("INSERT INTO kategorii (name) VALUES (?)", (item[0],))
            self.conn.commit()

    def add_expense(self, amount, cat_id):
        time = datetime.datetime.now()
        strok_data = time.strftime("%d.%m.%Y %H:%M")
        zp = "INSERT INTO rashodi (amount, cat_id, date) VALUES (?, ?, ?)"
        self.cursor.execute(zp, (amount, cat_id, strok_data))
        self.conn.commit()

    def delete_expense(self, id):
        zapros = "DELETE FROM rashodi WHERE id = ?"
        self.cursor.execute(zapros, (id,))
        self.conn.commit()

    def get_all_expenses(self):
        zapros = "SELECT r.id, r.amount, k.name, r.date FROM rashodi r JOIN kategorii k ON r.cat_id = k.id ORDER BY r.id DESC"
        self.cursor.execute(zapros)
        result = self.cursor.fetchall()
        return result

    def get_categories(self):
        self.cursor.execute("SELECT * FROM kategorii")
        return self.cursor.fetchall()

    def get_total_sum(self):
        self.cursor.execute("SELECT SUM(amount) FROM rashodi")
        itog = self.cursor.fetchone()[0]
        if itog == None:
            return 0
        return itog