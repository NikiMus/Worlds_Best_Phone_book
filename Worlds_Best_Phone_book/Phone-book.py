
from db import DB
from gui import GUI

db = DB()
gui = GUI(db)

if __name__ == "__main__":
    gui.run()


import sqlite3

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS contacts (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       phone TEXT,
                       email TEXT
                       );
        """)

        self.conn.commit()

    def get_contacts(self):
        self.c.execute('SELECT * FROM contacts')
        return self.c.fetchall()

    def add_contact(self, name, phone, email):
        self.c.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        self.conn.commit()

    def update_contact(self, id, name, phone, email):
        self.c.execute('UPDATE contacts SET name=?, phone=?, email=? WHERE id=?', (name, phone, email, id))
        self.conn.commit()

    def delete_contact(self, id):
        self.c.execute('DELETE FROM contacts WHERE id=?', (id,))
        self.conn.commit()

    def search_contacts(self, search_text):
        self.c.execute('SELECT * FROM contacts WHERE name LIKE ?', ('%' + search_text + '%',))
        return self.c.fetchall()


import tkinter as tk
from tkinter import ttk

class GUI():
    def __init__(self, db):
        self.db = db
        
    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title('Контакты')
        
        self.create_tree()
        
        self.show_contacts()
        
        self.add_button = tk.Button(self.root, text='Добавить', command=self.add_contact)
        self.add_button.pack()

        self.update_button = tk.Button(self.root, text='Обновить', command=self.update_contact)
        self.update_button.pack()

        self.delete_button = tk.Button(self.root, text='Удалить', command=self.delete_contacts)
        self.delete_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text='Поиск', command=self.search_contacts)
        self.search_button.pack()

        self.root.mainloop()

    def create_tree(self):
        self.tree = ttk.Treeview(self.root, columns=('name', 'phone', 'email'))
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        self.tree.heading('name', text='Имя')
        self.tree.column('name', width=100)
        self.tree.heading('phone', text='Телефон')
        self.tree.column('phone', width=100)
        self.tree.heading('email', text='Email')
        self.tree.column('email', width=150)
        self.tree.pack()

    def show_contacts(self):
        contacts = self.db.get_contacts()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for contact in contacts:
            self.tree.insert('', 'end', values=contact)

    def add_contact(self):
        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            self.db.add_contact(name, phone, email)
            self.show_contacts()
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title('Добавить контакт')
        name_label = tk.Label(add_window, text='Имя:')
        name_entry = tk.Entry(add_window)
        phone_label = tk.Label(add_window, text='Телефон:')
        phone_entry = tk.Entry(add_window)
        email_label = tk.Label(add_window, text='Email:')
        email_entry = tk.Entry(add_window)
        save_button = tk.Button(add_window, text='Сохранить', command=save_contact)
        name_label.pack()
        name_entry.pack()
        phone_label.pack()
        phone_entry.pack()
        email_label.pack()
        email_entry.pack()
        save_button.pack()

    def update_contact(self):
        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            self.db.update_contact(selected_id, name, phone, email)
            self.show_contacts()
            update_window.destroy()

        selected_item = self.tree.selection()[0]
        selected_id = self.tree.item(selected_item)['values'][0]
        contact = self.db.get_contact(selected_id)

        update_window = tk.Toplevel(self.root)
        update_window.title('Обновить контакт')
        name_label = tk.Label(update_window, text='Имя:')
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, contact[1])
        phone_label = tk.Label(update_window, text='Телефон:')
        phone_entry = tk.Entry(update_window)
        phone_entry.insert(0, contact[2])
        email_label = tk.Label(update_window, text='Email:')
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, contact[3])
        save_button = tk.Button(update_window, text='Сохранить', command=save_contact)
        name_label.pack()
        name_entry.pack()
        phone_label.pack()
        phone_entry.pack()
        email_label.pack()
        email_entry.pack()
        save_button.pack()

    def delete_contacts(self):
        for selected_item in self.tree.selection():
            selected_id = self.tree.item(selected_item)['values'][0]
            self.db.delete_contact(selected_id)
            self.tree.delete(selected_item)

    def search_contacts(self):
        search_text = self.search_entry.get()
        contacts = self.db.search_contacts(search_text)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for contact in contacts:
            self.tree.insert('', 'end', values=contact)

    def run(self):
        self.create_main_window()
