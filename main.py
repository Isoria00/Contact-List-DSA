import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3

# Root window
root = ctk.CTk()
root.title("Contact List")
root.geometry("700x700")

# Connect Data File to Program
def connect_db():
    return sqlite3.connect("contacts.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        birthday TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to clear the window of any existing widgets
def clear_window():
    for widget in root.winfo_children():
        widget.grid_forget()

# Fetch all contacts from the database
def get_all_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Actual working sort button this time 

def sort_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts ORDER BY name COLLATE NOCASE')
    sorted_contacts = cursor.fetchall()
    conn.close()

    
    clear_window()
    contact_list_frame = ctk.CTkFrame(root)
    contact_list_frame.grid(row=0, column=0, padx=10, pady=10)

    header = ctk.CTkLabel(contact_list_frame, text="Sorted Contacts", font=("Arial", 16))
    header.grid(row=0, columnspan=4, pady=10)

    row = 1
    for contact in sorted_contacts:
        name, phone, birthday = contact[1], contact[2], contact[3]
        contact_button = ctk.CTkButton(contact_list_frame, text=name, command=lambda name=name: show_contact_details(name))
        contact_button.grid(row=row, columnspan=2, pady=5)

        edit_button = ctk.CTkButton(contact_list_frame, hover_color="black",
        text_color="white", text="Edit", width=10, command=lambda name=name: edit_contact(name))
        edit_button.grid(row=row, column=2, padx=5)

        delete_button = ctk.CTkButton(contact_list_frame, hover_color="red", text="Delete", width=10, command=lambda name=name: delete_contact_action(name))
        delete_button.grid(row=row, column=3, padx=5)

        row += 1

    back_button = ctk.CTkButton(contact_list_frame, text="Back", command=show_contact_list)
    back_button.grid(row=row + 1, columnspan=4, pady=20)
    
    search_button = ctk.CTkButton(contact_list_frame, text="Search Contact", command=search_contact)
    search_button.grid(row=row + 2, columnspan=4, pady=10)

    print_button = ctk.CTkButton(contact_list_frame, text="Print Contacts", command=print_contacts)
    print_button.grid(row=row + 3, columnspan=4, pady=10)



# Add a new contact to the database
def add_contact(name, phone, birthday):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone, birthday) VALUES (?, ?, ?)', (name, phone, birthday))
    conn.commit()
    conn.close()

# Update contact in the database
def update_contact(old_name, new_name, new_phone, new_birthday):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE contacts
    SET name = ?, phone = ?, birthday = ?
    WHERE name = ?
    ''', (new_name, new_phone, new_birthday, old_name))
    conn.commit()
    conn.close()

# Delete a contact from the database
def delete_contact(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
    conn.commit()
    conn.close()

# Display the contact list
def show_contact_list():
    clear_window()
    contacts = get_all_contacts()

    contact_list_frame = ctk.CTkFrame(root)
    contact_list_frame.grid(row=0, column=0, padx=10, pady=10)

    header = ctk.CTkLabel(contact_list_frame, text="Contacts", font=("Arial", 16))
    header.grid(row=0, columnspan=4, pady=10)

    row = 1
    for contact in contacts:
        name, phone, birthday = contact[1], contact[2], contact[3]
        contact_button = ctk.CTkButton(contact_list_frame, text=name, command=lambda name=name: show_contact_details(name))
        contact_button.grid(row=row, columnspan=2, pady=5)

        edit_button = ctk.CTkButton(contact_list_frame, hover_color="black",
        text_color="white", text="Edit", width=10, command=lambda name=name: edit_contact(name))
        edit_button.grid(row=row, column=2, padx=5)

        delete_button = ctk.CTkButton(contact_list_frame, hover_color="red", text="Delete", width=10, command=lambda name=name: delete_contact_action(name))
        delete_button.grid(row=row, column=3, padx=5)

        row += 1

    add_contact_button = ctk.CTkButton(contact_list_frame, text="Add New Contact", command=add_contact_ui)
    add_contact_button.grid(row=row, columnspan=4, pady=20)

    sort_button = ctk.CTkButton(contact_list_frame, text="Sort Contacts", command=sort_contacts)
    sort_button.grid(row=row + 1, columnspan=4, pady=10)


    search_button = ctk.CTkButton(contact_list_frame, text="Search Contact", command=search_contact)
    search_button.grid(row=row + 2, columnspan=4, pady=10)

    print_button = ctk.CTkButton(contact_list_frame, text="Print Contacts", command=print_contacts)
    print_button.grid(row=row + 3, columnspan=4, pady=10)


def add_contact_ui():
    clear_window()

    name_label = ctk.CTkLabel(root, text="Name:")
    name_label.grid(row=0, column=0)
    name_entry = ctk.CTkEntry(root)
    name_entry.grid(row=0, column=1)

    phone_label = ctk.CTkLabel(root, text="Phone:")
    phone_label.grid(row=1, column=0)
    phone_entry = ctk.CTkEntry(root)
    phone_entry.grid(row=1, column=1)

    birthday_label = ctk.CTkLabel(root, text="Birthday:")
    birthday_label.grid(row=2, column=0)
    birthday_entry = ctk.CTkEntry(root)
    birthday_entry.grid(row=2, column=1)

    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        birthday = birthday_entry.get()
        if name and phone and birthday:
            add_contact(name, phone, birthday)
            show_contact_list()

    save_button = ctk.CTkButton(root, text="Save", command=save_contact)
    save_button.grid(row=3, columnspan=2, pady=20)

    back_button = ctk.CTkButton(root, text="Back", command=show_contact_list)
    back_button.grid(row=4, columnspan=2, pady=10)


def edit_contact(name):
    clear_window()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE name = ?', (name,))
    contact = cursor.fetchone()
    conn.close()

    if contact:
        name_label = ctk.CTkLabel(root, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = ctk.CTkEntry(root)
        name_entry.insert(0, contact[1])
        name_entry.grid(row=0, column=1)

        phone_label = ctk.CTkLabel(root, text="Phone:")
        phone_label.grid(row=1, column=0)
        phone_entry = ctk.CTkEntry(root)
        phone_entry.insert(0, contact[2])
        phone_entry.grid(row=1, column=1)

        birthday_label = ctk.CTkLabel(root, text="Birthday:")
        birthday_label.grid(row=2, column=0)
        birthday_entry = ctk.CTkEntry(root)
        birthday_entry.insert(0, contact[3])
        birthday_entry.grid(row=2, column=1)

        def save_edit():
            update_contact(contact[1], name_entry.get(), phone_entry.get(), birthday_entry.get())
            show_contact_list()

        save_button = ctk.CTkButton(root, text="Save", command=save_edit)
        save_button.grid(row=3, columnspan=2, pady=20)

        back_button = ctk.CTkButton(root, text="Back", command=show_contact_list)
        back_button.grid(row=4, columnspan=2, pady=10)


def delete_contact_action(name):
    if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {name}?"):
        delete_contact(name)
        show_contact_list()


def search_contact():
    clear_window()

    search_label = ctk.CTkLabel(root, text="Search:")
    search_label.grid(row=0, column=0)
    search_entry = ctk.CTkEntry(root)
    search_entry.grid(row=0, column=1)

    back_button = ctk.CTkButton(root, text="Back", command=show_contact_list)
    back_button.grid(row=4, columnspan=1, pady=10)

    def search():
        term = search_entry.get().lower()
        contacts = get_all_contacts()
        filtered = [c for c in contacts if term in c[1].lower()]
        clear_window()
        for i, contact in enumerate(filtered):
            ctk.CTkButton(root, text=contact[1], command=lambda n=contact[1]: show_contact_details(n)).grid(row=i, column=0)
        back_button = ctk.CTkButton(root, text="Back", command=show_contact_list)
        back_button.grid(row=4, columnspan=2, pady=10)

    search_button = ctk.CTkButton(root, text="Search", command=search)
    search_button.grid(row=1, column=1)

# Print all contacts
def print_contacts():
    contacts = get_all_contacts()
    for contact in contacts:
        print(f"Name: {contact[1]}, Phone: {contact[2]}, Birthday: {contact[3]}")

# Show contact details -  name, phone number and birthday
def show_contact_details(name):
    clear_window()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE name = ?', (name,))
    contact = cursor.fetchone()
    conn.close()

    if contact:
        name_label = ctk.CTkLabel(root, text=f"Name: {contact[1]}")
        name_label.grid(row=0, column=0)
        phone_label = ctk.CTkLabel(root, text=f"Phone: {contact[2]}")
        phone_label.grid(row=1, column=0)
        birthday_label = ctk.CTkLabel(root, text=f"Birthday: {contact[3]}")
        birthday_label.grid(row=2, column=0)

        back_button = ctk.CTkButton(root, text="Back", command=show_contact_list)
        back_button.grid(row=3, column=0)
    
    edit_button = ctk.CTkButton(root, hover_color="black",
    text_color="white", text="Edit", width=10, command=lambda name=name: edit_contact(name))
    edit_button.grid(row=2, column=2, padx=5)

# Start
create_table()
show_contact_list()
root.mainloop()