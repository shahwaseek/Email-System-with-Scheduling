import smtplib
import sqlite3
from tkinter import Tk, Label, Entry, Text, Button, Listbox, Scrollbar, messagebox, ttk, simpledialog

# Function to save an email template to the database
def save_template():
    template_subject = template_subject_entry.get()
    template_body = template_body_text.get("1.0", "end-1c")

    conn = sqlite3.connect("email_system.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS templates (subject TEXT, body TEXT)")
    cursor.execute("INSERT INTO templates VALUES (?, ?)", (template_subject, template_body))

    conn.commit()
    conn.close()

    # Reload templates in the listbox
    load_and_insert_templates()

# Function to load email templates from the database
def load_templates():
    conn = sqlite3.connect("email_system.db")
    cursor = conn.cursor()

    # Create the "templates" table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS templates (subject TEXT, body TEXT)")

    # Fetch templates from the database
    cursor.execute("SELECT * FROM templates")
    templates = cursor.fetchall()

    conn.close()

    return templates

# Function to load and insert templates into the listbox
def load_and_insert_templates():
    template_listbox.delete(0, 'end')  # Clear the existing listbox
    templates = load_templates()
    for template in templates:
        template_listbox.insert('end', template[0])

# Function to send emails to all addresses using the selected template
def send_emails():
    recipient_email = to_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", "end-1c")

    # Fetch the selected template
    selected_template = template_dropdown.get()

    if selected_template:
        # Fetch the template from the database based on the selected template
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM templates WHERE subject=?", (selected_template,))
        template = cursor.fetchone()

        conn.close()

        if template:
            subject = template[0]
            body = template[1]

    sender_email = "shahwaseek@gmail.com"
    sender_password = "ogaf vjxk sxxh bnrb"

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, recipient_email, message)

    messagebox.showinfo("Send Emails", "Email sent successfully!")

# Function to display all email addresses from the database in a new window
def display_addresses():
    addresses_window = Tk()
    addresses_window.title("Email Addresses")
    addresses_window.geometry("400x300")

    addresses_label = Label(addresses_window, text="Email Addresses:")
    addresses_label.pack(pady=(10, 5))

    addresses_listbox = Listbox(addresses_window, selectmode="single", height=10, width=40)
    addresses_listbox.pack(padx=10, pady=5)

    # Fetch and display all email addresses from the "email_system.db" database
    try:
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM addresses")
        addresses = cursor.fetchall()

        if addresses:
            for address in addresses:
                addresses_listbox.insert("end", address[0])

            # Function to select the address from the listbox
            def select_address():
                selected_index = addresses_listbox.curselection()
                if selected_index:
                    selected_address = addresses_listbox.get(selected_index)
                    to_entry.delete(0, 'end')
                    to_entry.insert(0, selected_address)
                    addresses_window.destroy()
                else:
                    messagebox.showerror("Select Address", "Error: No address selected.")

            # Add a button to select the address
            select_button = Button(addresses_window, text="Select", command=select_address)
            select_button.pack(pady=(5, 10))
        else:
            messagebox.showinfo("No Addresses", "No email addresses found in the database.")

    except sqlite3.Error as e:
        print("SQLite error:", e)
        messagebox.showerror("Database Error", "Error accessing the database.")

    finally:
        if conn:
            conn.close()

    addresses_window.mainloop()

# Function to copy text to clipboard
def copy_to_clipboard(text_to_copy):
    window.clipboard_clear()
    window.clipboard_append(text_to_copy)
    window.update()

# Function to add, edit, or remove email addresses
def manage_addresses():
    manage_window = Tk()
    manage_window.title("Manage Addresses")
    manage_window.geometry("400x300")

    address_label = Label(manage_window, text="Email Address:")
    address_label.grid(row=0, column=0, sticky="e")

    address_entry = Entry(manage_window)
    address_entry.grid(row=0, column=1, columnspan=2, sticky="we")

    add_button = Button(manage_window, text="Add", command=lambda: add_address(address_entry.get()))
    add_button.grid(row=1, column=0, pady=(10, 0))

    edit_button = Button(manage_window, text="Edit", command=lambda: edit_address(address_entry.get()))
    edit_button.grid(row=1, column=1, pady=(10, 0))

    remove_button = Button(manage_window, text="Remove", command=lambda: remove_address(address_entry.get()))
    remove_button.grid(row=1, column=2, pady=(10, 0))

    display_button = Button(manage_window, text="Display", command=display_addresses)
    display_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))

    manage_window.mainloop()

# Function to add an email address
def add_address(address):
    if address:
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO addresses VALUES (?)", (address,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Add Address", "Email address added successfully.")
        display_addresses()
    else:
        messagebox.showerror("Add Address", "Error: Enter a valid email address.")

# Function to load email addresses from the database
def load_addresses():
    conn = sqlite3.connect("email_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM addresses")
    addresses = cursor.fetchall()

    conn.close()

    return addresses

# Function to edit an email address
def edit_address(address):
    if address:
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM addresses WHERE email=?", (address,))
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        if result:
            new_address = simpledialog.askstring("Edit Address", "Enter the new email address:", initialvalue=address)

            if new_address:
                conn = sqlite3.connect("email_system.db")
                cursor = conn.cursor()

                cursor.execute("UPDATE addresses SET email=? WHERE email=?", (new_address, address))

                conn.commit()
                conn.close()

                messagebox.showinfo("Edit Address", "Email address edited successfully.")
                display_addresses()
        else:
            messagebox.showerror("Edit Address", "Error: Email address not found.")
    else:
        messagebox.showerror("Edit Address", "Error: Enter a valid email address.")

# Function to remove an email address
def remove_address(address):
    if address:
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM addresses WHERE email=?", (address,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Remove Address", "Email address removed successfully.")
        display_addresses()
    else:
        messagebox.showerror("Remove Address", "Error: Enter a valid email address.")

# Function to populate the template dropdown list in the "Send Emails" tab
def populate_template_dropdown():
    templates = load_templates()
    template_names = [template[0] for template in templates]
    template_dropdown['values'] = template_names

# Function to handle the selection of a template in the dropdown list
def on_template_selected(event):
    selected_template = template_dropdown.get()

    # Fetch the template from the database based on the selected template
    conn = sqlite3.connect("email_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM templates WHERE subject=?", (selected_template,))
    template = cursor.fetchone()

    conn.close()

    if template:
        subject_entry.delete(0, 'end')
        subject_entry.insert(0, template[0])

        body_text.delete("1.0", "end-1c")
        body_text.insert("1.0", template[1])

# Function to add an email address
def add_email():
    email = email_entry.get()
    add_address(email)

# Function to delete the selected template
def delete_template():
    selected_index = template_listbox.curselection()
    if selected_index:
        selected_template = template_listbox.get(selected_index)
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM templates WHERE subject=?", (selected_template,))
        conn.commit()
        conn.close()

        # Update the list of templates displayed
        load_and_insert_templates()
    else:
        messagebox.showerror("Delete Template", "Error: No template selected.")

# Function to select a template from the listbox in the "Manage Templates" tab
def select_template():
    selected_index = template_listbox.curselection()
    if selected_index:
        selected_template = template_listbox.get(selected_index)
        conn = sqlite3.connect("email_system.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM templates WHERE subject=?", (selected_template,))
        template = cursor.fetchone()

        conn.close()

        if template:
            subject_entry.delete(0, 'end')
            subject_entry.insert(0, template[0])

            body_text.delete("1.0", "end-1c")
            body_text.insert("1.0", template[1])
    else:
        messagebox.showerror("Select Template", "Error: No template selected.")

# Create the GUI window
window = Tk()
window.title("Automatic Email And Management")
window.geometry("800x600")

# Create a Notebook (Tabbed interface)
notebook = ttk.Notebook(window)

# Tab for sending emails
send_email_frame = ttk.Frame(notebook)

to_label = Label(send_email_frame, text="To:")
to_label.grid(row=0, column=0, sticky="e")

to_entry = Entry(send_email_frame)
to_entry.grid(row=0, column=1, columnspan=2, sticky="we")

# Button to load saved addresses
load_addresses_button = Button(send_email_frame, text="Load Saved Addresses", command=display_addresses)
load_addresses_button.grid(row=0, column=3)

subject_label = Label(send_email_frame, text="Subject:")
subject_label.grid(row=1, column=0, sticky="e")

subject_entry = Entry(send_email_frame)
subject_entry.grid(row=1, column=1, columnspan=2, sticky="we")

body_label = Label(send_email_frame, text="Body:")
body_label.grid(row=2, column=0, sticky="ne")

body_text = Text(send_email_frame, wrap="word", height=5, width=40)
body_text.grid(row=2, column=1, columnspan=2, sticky="we")

# Dropdown list for templates in the "Send Emails" tab
template_dropdown_label = Label(send_email_frame, text="Select Template:")
template_dropdown_label.grid(row=3, column=0, sticky="e")

template_dropdown = ttk.Combobox(send_email_frame, state="readonly")
template_dropdown.grid(row=3, column=1, columnspan=2, sticky="we")
populate_template_dropdown()  # Populate the dropdown list initially
template_dropdown.bind("<<ComboboxSelected>>", on_template_selected)  # Bind event handler

send_button = Button(send_email_frame, text="Send Emails", command=send_emails)
send_button.grid(row=4, column=0, columnspan=3)

notebook.add(send_email_frame, text="Send Emails")

# Tab for managing templates
manage_templates_frame = ttk.Frame(notebook)

template_label = Label(manage_templates_frame, text="Templates:")
template_label.grid(row=0, column=0, columnspan=3, pady=(20, 5))

template_listbox = Listbox(manage_templates_frame, selectmode="single", height=6, width=40)
template_listbox.grid(row=1, column=0, columnspan=3)

load_templates_button = Button(manage_templates_frame, text="Load Templates", command=lambda: load_and_insert_templates())
load_templates_button.grid(row=2, column=0, columnspan=3)

select_template_button = Button(manage_templates_frame, text="Select Template", command=select_template)
select_template_button.grid(row=3, column=0, columnspan=3)

template_subject_label = Label(manage_templates_frame, text="Subject:")
template_subject_label.grid(row=6, column=0, sticky="e")

template_subject_entry = Entry(manage_templates_frame)
template_subject_entry.grid(row=6, column=1, columnspan=2, sticky="we")

template_body_label = Label(manage_templates_frame, text="Body:")
template_body_label.grid(row=7, column=0, sticky="ne")

template_body_text = Text(manage_templates_frame, wrap="word", height=5, width=40)
template_body_text.grid(row=7, column=1, columnspan=2, sticky="we")

save_template_button = Button(manage_templates_frame, text="Save Template", command=save_template)
save_template_button.grid(row=8, column=0, columnspan=3)

template_label = Label(manage_templates_frame, text="Save Template:")
template_label.grid(row=5, column=0, columnspan=3, pady=(20, 5))


# Add the delete button to the "Manage Templates" page
delete_template_button = Button(manage_templates_frame, text="Delete Template", command=delete_template)
delete_template_button.grid(row=4, column=0, columnspan=3 )

notebook.add(manage_templates_frame, text="Manage Templates")

# Tab for managing email addresses
manage_addresses_frame = ttk.Frame(notebook)

email_label = Label(manage_addresses_frame, text="Email Address:")
email_label.grid(row=0, column=0, sticky="e")

email_entry = Entry(manage_addresses_frame)
email_entry.grid(row=0, column=1, columnspan=2, sticky="we")

save_email_button = Button(manage_addresses_frame, text="Save Email", command=add_email)
save_email_button.grid(row=1, column=0, columnspan=3)

load_addresses_button = Button(manage_addresses_frame, text="Load Addresses", command=lambda: print(load_addresses()))
load_addresses_button.grid(row=2, column=0, columnspan=3)

display_addresses_button = Button(manage_addresses_frame, text="Display Addresses", command=display_addresses)
display_addresses_button.grid(row=3, column=0, columnspan=3)

manage_addresses_button = Button(manage_addresses_frame, text="Manage Addresses", command=manage_addresses)
manage_addresses_button.grid(row=4, column=0, columnspan=3)

notebook.add(manage_addresses_frame, text="Manage Addresses")

# Pack the Notebook to make it visible
notebook.pack(expand=1, fill="both")

window.mainloop()
