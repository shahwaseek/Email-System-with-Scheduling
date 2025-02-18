import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class HistoryTab:
    def __init__(self, parent, cursor):
        self.parent = parent
        self.cursor = cursor

        self.history_tab = ttk.Frame(self.parent)
        self.display_history_button = tk.Button(self.history_tab, text="Display History", command=self.display_history)
        self.display_history_button.pack()

        self.history_text = tk.Text(self.history_tab, height=20, width=80)
        self.history_text.pack()

        self.history_tab.pack()

    def display_history(self):
        self.cursor.execute("SELECT email, sent_at FROM history")
        history = self.cursor.fetchall()
        history_str = "Mail Sent History:\n"
        for record in history:
            history_str += f"Email: {record[0]}, Sent At: {record[1]}\n"
        self.history_text.delete('1.0', tk.END)
        self.history_text.insert(tk.END, history_str)

class EmailSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Email System")
        self.root.geometry("800x600")

        # Create a database connection
        self.conn = sqlite3.connect("email_database.db")
        self.cursor = self.conn.cursor()

        # Create tables if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                email TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

        # Tabs
        self.tabs = ttk.Notebook(self.root)

        # History Tab
        self.history_tab = HistoryTab(self.tabs, self.cursor)
        self.tabs.add(self.history_tab.history_tab, text="History")

        self.tabs.pack(expand=1, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSystem(root)
    root.mainloop()
