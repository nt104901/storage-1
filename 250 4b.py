import tkinter as tk
from tkinter import ttk
import datetime

class PortfolioManager:
    def __init__(self, master):
        self.master = master
        master.title("Финансовый Менеджер")

        # Данные портфеля (можно заменить на базу данных)
        self.portfolio = {
            "AAPL": {"name": "Apple Inc.", "quantity": 0, "price": 0},
            "GOOG": {"name": "Alphabet Inc.", "quantity": 0, "price": 0},
            "MSFT": {"name": "Microsoft Corp.", "quantity": 0, "price": 0},
            "TSLA": {"name": "Tesla Inc.", "quantity": 0, "price": 0},
        }

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # Label
        tk.Label(self.master, text="Финансовый Менеджер Портфеля").pack(pady=10)

        # Кнопки для добавления активов
        add_button = tk.Button(self.master, text="Добавить Активы", command=self.add_asset)
        add_button.pack(pady=5)

        # Treeview для отображения активов
        self.tree = ttk.Treeview(self.master, columns=("Name", "Quantity", "Price"), show="headings")
        self.tree.heading("Name", text="Название")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Price", text="Цена")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Ввод данных для активов
        self.name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()

        name_label = tk.Label(self.master, text="Название актива:")
        name_label.pack()
        name_entry = tk.Entry(self.master, textvariable=self.name_var)
        name_entry.pack()

        quantity_label = tk.Label(self.master, text="Количество:")
        quantity_label.pack()
        quantity_entry = tk.Entry(self.master, textvariable=self.quantity_var)
        quantity_entry.pack()

        price_label = tk.Label(self.master, text="Цена:")
        price_label.pack()
        price_entry = tk.Entry(self.master, textvariable=self.price_var)
        price_entry.pack()

        # Кнопка для добавления актива в портфель
        add_asset_button = tk.Button(self.master, text="Добавить", command=self.add_asset_from_entry)
        add_asset_button.pack(pady=5)

        # Кнопка для удаления актива
        delete_button = tk.Button(self.master, text="Удалить Активы", command=self.delete_asset)
        delete_button.pack(pady=5)

    def add_asset(self):
        name = self.name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()

        if name and quantity and price:
            if name in self.portfolio:
                self.portfolio[name]["quantity"] = quantity
                self.portfolio[name]["price"] = price
            else:
                self.portfolio[name] = {"name": name, "quantity": quantity, "price": price}
            self.update_treeview()
            self.clear_entry_fields()

    def add_asset_from_entry(self):
        name = self.name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()

        if name and quantity and price:
            if name in self.portfolio:
                self.portfolio[name]["quantity"] = quantity
                self.portfolio[name]["price"] = price
            else:
                self.portfolio[name] = {"name": name, "quantity": quantity, "price": price}
            self.update_treeview()
            self.clear_entry_fields()

    def delete_asset(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)['values']
            asset_name = item_values[0]
            del self.portfolio[asset_name]
            self.update_treeview()
            self.clear_entry_fields()

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for asset, data in self.portfolio.items():
            self.tree.insert("", tk.END, values=(data["name"], data["quantity"], data["price"]))

    def clear_entry_fields(self):
        self.name_var.set("")
        self.quantity_var.set(0)
        self.price_var.set(0.0)

root = tk.Tk()
portfolio_manager = PortfolioManager(root)
root.mainloop()
