import tkinter as tk
from tkinter import messagebox
import os

def authenticate():
    password = password_entry.get()
    if password == "2148":
        os.system('python main.py')
        messagebox.showinfo("Success", "Login Successful.")
    else:
        messagebox.showerror("Error", "Incorrect password. Try again.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Login")

# Create labels and entry widgets
password_label = tk.Label(root, text="Password:")
password_label.grid(row=0, column=0, padx=5, pady=5)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=0, column=1, padx=5, pady=5)

# Create login button
login_button = tk.Button(root, text="Login", command=authenticate)
login_button.grid(row=1, columnspan=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
