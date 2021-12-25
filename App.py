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
app = None


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


        """
        key is query, value is another dict containing columns and entries
        example output would be:
        self.output_queries = {
            "SELECT * FROM customer WHERE STATE==Canada":  {
                    "column_names" = [.....],
                    "entries" = [....]
                },
            ....        
        }
        """

        self.output_queries = {}

        self.selected_table_name = None

        self.table_list = tk.Listbox(root)
        self.table_list["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.table_list["font"] = ft
        self.table_list["fg"] = "#333333"
        self.table_list["justify"] = "center"
        self.table_list.place(x=0, y=260, width=181, height=234)
        self.table_list.bind('<<ListboxSelect>>', self.table_list_select_click)

        self.populate_box(self.table_list, tables_list)



        table_lists_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        table_lists_label["font"] = ft
        table_lists_label["fg"] = "#333333"
        table_lists_label["justify"] = "center"
        table_lists_label["text"] = "Tables List"
        table_lists_label.place(x=0,y=235,width=181,height=30)

        tables_after_operations_label = tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        tables_after_operations_label["font"] = ft
        tables_after_operations_label["fg"] = "#333333"
        tables_after_operations_label["justify"] = "center"
        tables_after_operations_label["text"] = "Tables After Operations"
        tables_after_operations_label.place(x=418,y=235,width=181,height=30)
        
        tables_after_operations_list=tk.Listbox(root)
        tables_after_operations_list["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        tables_after_operations_list["font"] = ft
        tables_after_operations_list["fg"] = "#333333"
        tables_after_operations_list["justify"] = "center"
        tables_after_operations_list.place(x=418,y=260,width=181,height=234)

        select_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        select_label["font"] = ft
        select_label["fg"] = "#333333"
        select_label["justify"] = "center"
        select_label["text"] = "SELECT"
        select_label.place(x=190,y=260,width=100,height=30)

        self.select_text = tk.Text(root)
        self.select_text["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.select_text["font"] = ft
        self.select_text["fg"] = "#333333"
        self.select_text.place(x=280,y=260,width=100,height=30)

        from_label = tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        from_label["font"] = ft
        from_label["fg"] = "#333333"
        from_label["justify"] = "center"
        from_label["text"] = "FROM"
        from_label.place(x=190,y=310,width=100,height=30)

        self.from_table_text = tk.StringVar()
        self.from_table_text.set("")

        self.from_table_label = tk.Label(root, textvariable=self.from_table_text)
        self.from_table_label["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.from_table_label["font"] = ft
        self.from_table_label["fg"] = "#333333"
        from_label["justify"] = "center"
        self.from_table_label.place(x=280, y=310, width=100, height=30)

        where_label = tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        where_label["font"] = ft
        where_label["fg"] = "#333333"
        where_label["justify"] = "center"
        where_label["text"] = "WHERE"
        where_label.place(x=190,y=360,width=100,height=30)

        self.where_text = tk.Text(root)
        self.where_text["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.where_text["font"] = ft
        self.where_text["fg"] = "#333333"
        self.where_text.place(x=280,y=360,width=100,height=80)

        execute_button = tk.Button(root)
        execute_button["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        execute_button["font"] = ft
        execute_button["fg"] = "#000000"
        execute_button["justify"] = "center"
        execute_button["text"] = "Execute"
        execute_button.place(x=280,y=450,width=70,height=25)
        execute_button["command"] = self.execute_query

    def get_listbox(self):
        return self.table_list

    def execute_query(self):
        if self.selected_table_name == "" or self.selected_table_name is None:
            return

        select_val = self.select_text.get("1.0", tk.END).replace("\n", " ")
        from_val = self.from_table_text.get()
        where_val = self.where_text.get("1.0", tk.END).replace("\n", " ")

        if select_val == " " or from_val == "":
            self.select_text.insert(tk.INSERT, "INVALID")
            self.where_text.insert(tk.INSERT, "INVALID")

        query_str = f"SELECT {select_val} FROM {from_val}"
        if where_val != " ":
            query_str += f" WHERE {where_val}"


        #TODO try catch on this method, this would happen probably on invalid query,
        # in this case we should put invalid query inside select and where text
        entries = createCsvFromDb.execute_query(from_val, query_str)

        #TODO get the columns of the query into a list
        columns = []

        # this would override old query
        self.output_queries[query_str] = {
            "columns": columns,
            "entries": entries
        }

        #TODO add query_str to table operatrions list

        #TODO add when clicked on table operation list, display the query based on what was saved in output_queries

        #TODO add when right clicked on table operation list, remove query from table list and from output queries


    def table_list_select_click(self, event):
        treeFunctions.clear_tree(tree_view)
        treeFunctions.remove_columns(tree_view, tree_view['columns'])
        self.selected_table_name = self.table_list.get(self.table_list.curselection())

        # update query from table label
        self.from_table_text.set(self.selected_table_name)

        columns_names = createCsvFromDb.extract_table_column_names(self.selected_table_name)
        entries = createCsvFromDb.extract_entries_from_table(self.selected_table_name)

        treeFunctions.add_columns(tree_view, columns_names)
        for row in entries:
            tree_view.insert("", tk.END, values=row)

        tree_view.update()

        cols = tree_view['columns']
        for col in cols:
            tree_view.column(col, width=100, minwidth=110)  # restore to desired size

    def populate_box(self, mylistbox, list):
        for i in list:
            mylistbox.insert("end", i)


def configure_scrollbars():
    x_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    y_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree_view.configure(yscrollcommand=y_scrollbar.set)
    tree_view.configure(xscrollcommand=x_scrollbar.set)
    tree_view.pack()

    for col in tree_view['columns']:
        tree_view.heading(col, text=f"{col}", anchor=tk.CENTER)
        tree_view.column(col, anchor=tk.CENTER, width=40)  # initially smaller size
    tree_view.update()
    for col in tree_view['columns']:
        tree_view.column(col, width=100)  # restore to desired size

    x_scrollbar['command'] = tree_view.xview
    y_scrollbar['command'] = tree_view.yview

if __name__ == "__main__":
    createCsvFromDb.csv_from_db_init()
    createCsvFromDb.main()

    max_num_columns = createCsvFromDb.extract_max_columns()
    tables_list = createCsvFromDb.extract_table_names()
    columns = ["" for i in range(max_num_columns)]

    root = tk.Tk()
    app = App(root)
    tree_view = ttk.Treeview(root, columns=(), show='headings', selectmode='extended')

    configure_scrollbars()

    treeFunctions.add_columns(tree_view, columns)
    root.mainloop()
    createCsvFromDb.csv_from_db_destroy()
