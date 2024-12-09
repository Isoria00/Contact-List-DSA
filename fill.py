import sqlite3
import tkinter.messagebox as messagebox


# First Run main.py to create your contacts.db file!!!!!

# Run this program if you want to fill the Contact List with data. Make sure your file with the data is named "contacts.db"
contacts = {
    "Sean Strickland": {"Phone": "123-456-7890", "Birthday": "02/27/1991"},
    "Charles Oliveira": {"Phone": "987-654-3210", "Birthday": "10/17/1989"},
    "Jon Jones": {"Phone": "555-555-5555", "Birthday": "07/19/1987"},
    "Sean O'Malley": {"Phone": "444-444-4444", "Birthday": "10/24/1994"},
    "Dricus Du Plessis": {"Phone": "333-333-3333", "Birthday": "01/14/1994"},
    "Max Holloway": {"Phone": "222-222-2222", "Birthday": "12/04/1991"},
    "Ilia Topuria": {"Phone": "666-666-6666", "Birthday": "06/21/1996"},
    "Diego Lopez": {"Phone": "777-777-7777", "Birthday": "09/04/1996"},
    "Belal Muhammad": {"Phone": "888-888-8888", "Birthday": "07/09/1988"},
    "Alex Pereira": {"Phone": "999-999-9999", "Birthday": "07/07/1987"},
}

def connect_db():
    return sqlite3.connect("contacts.db")

def add_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    
    for name, details in contacts.items():
        cursor.execute(
            "INSERT INTO contacts (name, phone, birthday) VALUES (?, ?, ?)",
            (name, details["Phone"], details["Birthday"])
        )
    
    conn.commit()
    conn.close()
    print("Contacts added successfully.")
    messagebox.showinfo("Success", "Contacts added successfully! Run the Contact List Application!")
    

if __name__ == "__main__":
    add_contacts()
