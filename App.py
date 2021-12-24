import sqlite3
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import csv

import createCsvFromDb
import treeFunctions

import sys

root = None
tree_view = None
tables_list = None


def click_event(event):
    treeFunctions.clear_tree(tree_view)
    treeFunctions.remove_columns(tree_view, tree_view['columns'])
    table_name = app.get_listbox().get(app.get_listbox().curselection())

    columns_names = createCsvFromDb.extract_table_column_names(table_name)
    entries = createCsvFromDb.extract_entries_from_table(table_name)

    treeFunctions.add_columns(tree_view, columns_names)
    for row in entries:
        tree_view.insert("", tk.END, values=row)
    tree_view.update()
    cols = tree_view['columns']
    for col in cols:
        tree_view.column(col, width=100)  # restore to desired size




def populate_box(mylistbox, list):
    for i in list:
        mylistbox.insert("end", i)

class App:
    def __init__(self, root):
        # setting title
        root.title("Seminar Project")
        # setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_682=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_682["font"] = ft
        GLabel_682["fg"] = "#333333"
        GLabel_682["justify"] = "center"
        GLabel_682["text"] = "Display"
        GLabel_682.place(x=0,y=0,width=599,height=20)

        self.GListBox_280 = tk.Listbox(root)
        self.GListBox_280["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GListBox_280["font"] = ft
        self.GListBox_280["fg"] = "#333333"
        self.GListBox_280["justify"] = "center"
        self.GListBox_280.place(x=0,y=260,width=181,height=234)
        populate_box(self.GListBox_280, tables_list)

        GListBox_487=tk.Listbox(root)
        GListBox_487["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_487["font"] = ft
        GListBox_487["fg"] = "#333333"
        GListBox_487["justify"] = "center"
        GListBox_487.place(x=418,y=260,width=181,height=234)

        GLabel_16=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_16["font"] = ft
        GLabel_16["fg"] = "#333333"
        GLabel_16["justify"] = "center"
        GLabel_16["text"] = "Tables List"
        GLabel_16.place(x=0,y=230,width=181,height=30)

        GLabel_530=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_530["font"] = ft
        GLabel_530["fg"] = "#333333"
        GLabel_530["justify"] = "center"
        GLabel_530["text"] = "Tables After Operations"
        GLabel_530.place(x=418,y=230,width=181,height=30)

        GLabel_364=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_364["font"] = ft
        GLabel_364["fg"] = "#333333"
        GLabel_364["justify"] = "center"
        GLabel_364["text"] = "SELECT"
        GLabel_364.place(x=190,y=260,width=80,height=30)

        GListBox_935=tk.Listbox(root)
        GListBox_935["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_935["font"] = ft
        GListBox_935["fg"] = "#333333"
        GListBox_935["justify"] = "center"
        GListBox_935.place(x=280,y=260,width=80,height=30)

        GLabel_490=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_490["font"] = ft
        GLabel_490["fg"] = "#333333"
        GLabel_490["justify"] = "center"
        GLabel_490["text"] = "FROM"
        GLabel_490.place(x=190,y=310,width=80,height=30)

        GListBox_847=tk.Listbox(root)
        GListBox_847["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_847["font"] = ft
        GListBox_847["fg"] = "#333333"
        GListBox_847["justify"] = "center"
        GListBox_847.place(x=280,y=310,width=80,height=30)

        GLabel_161=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_161["font"] = ft
        GLabel_161["fg"] = "#333333"
        GLabel_161["justify"] = "center"
        GLabel_161["text"] = "OPERATION"
        GLabel_161.place(x=190,y=360,width=80,height=30)

        GListBox_907=tk.Listbox(root)
        GListBox_907["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_907["font"] = ft
        GListBox_907["fg"] = "#333333"
        GListBox_907["justify"] = "center"
        GListBox_907.place(x=280,y=360,width=80,height=30)

        GListBox_713=tk.Listbox(root)
        GListBox_713["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_713["font"] = ft
        GListBox_713["fg"] = "#333333"
        GListBox_713["justify"] = "center"
        GListBox_713.place(x=210,y=400,width=60,height=25)

        GListBox_421=tk.Listbox(root)
        GListBox_421["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_421["font"] = ft
        GListBox_421["fg"] = "#333333"
        GListBox_421["justify"] = "center"
        GListBox_421.place(x=280,y=400,width=60,height=25)

        GLineEdit_799=tk.Entry(root)
        GLineEdit_799["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_799["font"] = ft
        GLineEdit_799["fg"] = "#333333"
        GLineEdit_799["justify"] = "center"
        GLineEdit_799["text"] = "Entry"
        GLineEdit_799.place(x=350,y=400,width=60,height=25)

        GButton_243=tk.Button(root)
        GButton_243["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_243["font"] = ft
        GButton_243["fg"] = "#000000"
        GButton_243["justify"] = "center"
        GButton_243["text"] = "Execute"
        GButton_243.place(x=280,y=450,width=70,height=25)
        GButton_243["command"] = self.GButton_243_command

    def get_listbox(self):
        return self.GListBox_280

    def GButton_243_command(self):
        print("command")


def configure_scrollbars():
    x_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    x_scrollbar.grid(row=1, column=0, sticky=tk.E + tk.W)
    y_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    y_scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

    tree_view.configure(yscrollcommand=y_scrollbar.set)
    tree_view.configure(xscrollcommand=x_scrollbar.set)
    tree_view.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    for col in tree_view['columns']:
        tree_view.heading(col, text=f"{col}", anchor=tk.CENTER)
        tree_view.column(col, anchor=tk.CENTER, width=40)  # initially smaller size
    tree_view.update()
    for col in tree_view['columns']:
        tree_view.column(col, width=100)  # restore to desired size

    x_scrollbar['command'] = tree_view.xview
    y_scrollbar['command'] = tree_view.yview

if __name__ == "__main__":
    createCsvFromDb.main()

    max_num_columns = createCsvFromDb.extract_max_columns()
    tables_list = createCsvFromDb.extract_table_names()
    columns = ["" for i in range(max_num_columns)]

    root = tk.Tk()
    app = App(root)
    tree_view = ttk.Treeview(root, columns=(), show='headings', selectmode='browse')

    configure_scrollbars()

    treeFunctions.add_columns(tree_view, columns)
    app.get_listbox().bind('<<ListboxSelect>>', click_event)
    root.mainloop()
