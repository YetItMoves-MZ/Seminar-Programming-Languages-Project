from tkinter import ttk

import queries
import tkinter as tk

import sqlite3

import createCsvFromDb


def click_event(event):
    con1 = sqlite3.connect('chinook.db')
    cur1 = con1.cursor()
    listbox.get(listbox.curselection())
    cur1.execute(f"SELECT * FROM {listbox.get(listbox.curselection())}")
    rows = cur1.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    con1.close()


def populate_box(mylistbox):
    tables_list = ['albums', 'artists', 'customers', 'employees',
                   'genres', 'invoice_items','invoices', 'media_types',
                   'playlist_track', 'playlists', 'sqlite_sequence',
                   'sqlite_stat1', 'tracks']
    for i in tables_list:
        mylistbox.insert("end", i)


def reset():
    con1 = sqlite3.connect('chinook.db')
    cur1 = con1.cursor()
    cur1.execute(f"SELECT * FROM {value}")
    rows = cur1.fetchall()

    for row in rows:

        tree.insert("", tk.END, values=row)

    con1.close()


# connect to the database
createCsvFromDb.main()
root = tk.Tk()

tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="FNAME")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="LNAME")

tree.pack()

button1 = tk.Button(text="Display data", command=reset)
button1.pack(pady=10)

listbox = tk.Listbox(root)
listbox.pack(pady=20)
populate_box(listbox)
listbox.bind('<<ListboxSelect>>', click_event)

root.mainloop()
