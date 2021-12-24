import treeFunctions
import tkinter as tk

import sqlite3


def click_event(event):
    treeFunctions.clear_tree(tree)
    con1 = sqlite3.connect('database/chinook.db')
    cur1 = con1.cursor()
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


# def reset():
#     treeFunctions.clear_tree(tree)


# connect to the database
#createCsvFromDb.main()
    # root = tk.Tk()
    #
    # tree = ttk.Treeview(root, column=(), show='headings')
    # tree.pack()
    #
    #
    # button1 = tk.Button(text="Clear Data", command=reset)
    # button1.pack(pady=10)
    #
    # listbox = tk.Listbox(root)
    # listbox.pack(pady=20)
    # populate_box(listbox)
    # listbox.bind('<<ListboxSelect>>', click_event)
    #
    # root.mainloop()
