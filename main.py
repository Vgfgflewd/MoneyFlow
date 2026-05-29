import customtkinter as ctk
from tkinter import ttk, messagebox
from database import FinanceDB

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MoneyFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = FinanceDB()

        self.title("MoneyFlow")
        self.geometry("600x750")
        self.grid_columnconfigure(0, weight=1)

        # --- Заголовок и ОБЩАЯ СУММА ---
        self.header = ctk.CTkLabel(self, text= "MoneyFlow", font=("Segoe UI", 28, "bold"), text_color="#3b8ed0")
        self.header.grid(row=0, column=0, pady=(20, 5))

        # Виджет для вывода суммы
        self.total_label = ctk.CTkLabel(self, text="Итого: 0.00 ₽", font=("Segoe UI", 20, "bold"))
        self.total_label.grid(row=1, column=0, pady=(0, 20))

        # --- Фрейм ввода ---
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.amount_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Сумма...", width=250, height=40)
        self.amount_entry.grid(row=0, column=0, pady=(20, 10), padx=20)

        self.categories = self.db.get_categories()
        cat_names = [c[1] for c in self.categories]
        self.cat_menu = ctk.CTkOptionMenu(self.input_frame, values=cat_names, width=250, height=40)
        self.cat_menu.grid(row=1, column=0, pady=10, padx=20)

        self.add_btn = ctk.CTkButton(self.input_frame, text="Добавить расход", command=self.save_data, height=45)
        self.add_btn.grid(row=2, column=0, pady=(10, 20), padx=20)

        # --- Таблица ---
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b",
                             borderwidth=0, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#333333", foreground="white", relief="flat")
        self.style.map("Treeview", background=[('selected', '#1f538d')])

        cols = ("ID", "Сумма", "Категория", "Дата")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.grid(row=3, column=0, padx=30, pady=10, sticky="nsew")

        # --- Кнопка удаления ---
        self.delete_btn = ctk.CTkButton(self, text="Удалить выбранное", command=self.delete_data,
                                        fg_color="#a13232", hover_color="#7a2525", height=40)
        self.delete_btn.grid(row=4, column=0, pady=20)

        self.refresh_table()

    def save_data(self):
        try:
            amount = float(self.amount_entry.get().replace(',', '.'))
            if amount <= 0: raise ValueError

            selected_cat = self.cat_menu.get()
            cat_id = next(c[0] for c in self.categories if c[1] == selected_cat)

            self.db.add_expense(amount, cat_id)
            self.amount_entry.delete(0, 'end')
            self.refresh_table()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")

    def delete_data(self):
        # Получаем выбранную строку в таблице
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        # Берем ID из первой колонки выбранной строки
        item_id = self.tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Подтверждение", "Удалить эту запись?"):
            self.db.delete_expense(item_id)
            self.refresh_table()

    def refresh_table(self):
        # 1. Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)

        # 2. Загрузка данных
        for row in self.db.get_all_expenses():
            self.tree.insert("", "end", values=row)

        # 3. Обновление итоговой суммы
        total = self.db.get_total_sum()
        self.total_label.configure(text=f"Итого: {total:,.2f} ₽".replace(',', ' '))


if __name__ == "__main__":
    app = MoneyFlowApp()
    app.mainloop()