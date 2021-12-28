import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import createCsvFromDb
import treeFunctions


root = None
tree_view = None
tables_list = None
app = None


class App:
    def __init__(self, root):
        root.title("Seminar Project")
        width = 600
        height = 520
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times', size=10)

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
        self.table_list["font"] = ft
        self.table_list["justify"] = "center"
        self.table_list.place(x=5, y=265, width=170, height=230)
        self.table_list.bind('<<ListboxSelect>>', self.table_list_select_click)
        populate_listbox(self.table_list, tables_list)

        self.table_lists_label=tk.Label(root)
        self.table_lists_label["font"] = ft
        self.table_lists_label["justify"] = "center"
        self.table_lists_label["text"] = "Tables List"
        self.table_lists_label.place(x=0, y=235, width=180, height=30)

        self.tables_filter_Label = tk.Label(root)
        self.tables_filter_Label["font"] = ft
        self.tables_filter_Label["justify"] = "center"
        self.tables_filter_Label["text"] = "Tables Filter"
        self.tables_filter_Label.place(x=405, y=235, width=180, height=30)
        
        self.tables_filter_List = tk.Listbox(root)
        self.tables_filter_List["font"] = ft
        self.tables_filter_List["justify"] = "center"
        self.tables_filter_List.place(x=410, y=265, width=170, height=230)

        self.column_label = tk.Label(root)
        self.column_label["font"] = ft
        self.column_label["justify"] = "center"
        self.column_label["text"] = "Column"
        self.column_label.place(x=175, y=260, width=100, height=30)

        self.column_choices = ()
        self.column_clicked = tk.StringVar(root)
        self.column_checkbox = tk.OptionMenu(root, self.column_clicked, self.column_choices)
        self.column_checkbox["font"] = ft
        self.column_checkbox.place(x=255, y=260, width=130, height=30)

        self.operation_label = tk.Label(root)
        self.operation_label["font"] = ft
        self.operation_label["justify"] = "center"
        self.operation_label["text"] = "Operation"
        self.operation_label.place(x=175, y=300, width=100, height=30)

        self.operation_choices = ()
        self.operation_clicked = tk.StringVar(root)
        self.operation_checkbox = tk.OptionMenu(root, self.operation_clicked, self.operation_choices)
        self.operation_checkbox["font"] = ft
        self.operation_checkbox.place(x=255, y=300, width=130, height=30)

        self.value_label = tk.Label(root)
        self.value_label["font"] = ft
        self.value_label["justify"] = "center"
        self.value_label["text"] = "Value"
        self.value_label.place(x=175, y=340, width=100, height=30)

        self.value_text = tk.Text(root)
        self.value_text["font"] = ft
        self.value_text.place(x=255, y=340, width=130, height=30)

        self.case_sensitive_label = tk.Label(root)
        self.case_sensitive_label["font"] = ft
        self.case_sensitive_label["justify"] = "center"
        self.case_sensitive_label["text"] = "Case Sensitive"
        self.case_sensitive_label.place(x=175, y=380, width=100, height=30)

        self.case_sensitive_choice = tk.IntVar()
        self.case_sensitive_checkbox = tk.Checkbutton(root, variable=self.case_sensitive_choice, onvalue=1, offvalue=0)
        self.case_sensitive_checkbox.place(x=270, y=380, width=20, height=30)

        self.execute_button = tk.Button(root)
        self.execute_button["font"] = ft
        self.execute_button["justify"] = "center"
        self.execute_button["text"] = "Execute"
        self.execute_button.place(x=315, y=380, width=70, height=25)
        self.execute_button["command"] = self.execute_query

        self.error_message_text = tk.Text(root)
        self.error_message_text["font"] = ft
        self.error_message_text.place(x=255, y=420, width=130, height=30)

    def get_listbox(self):
        return self.table_list

    def execute_query(self):
        if self.selected_table_name == "" or self.selected_table_name is None:
            return

        column_val = self.column_clicked.get()
        operation_val = self.operation_clicked.get()
        input_val = self.value_text.get("1.0", tk.END)
        case_sensitive_val = self.case_sensitive_choice.get()

        while input_val.endswith('\n'):
            # Drop last blank line which textbox automatically inserts.
            # User may have manually deleted during edit so don't always assume
            input_val = input_val[:-1]

        # is_valid = createCsvFromDb.is_select_match_input(self.selected_table_name, select_choice)
        # if not is_valid == type(input_val):
        #     self.error_message_text.insert(tk.INSERT, "Invalid Column and Value Type")

        # TODO its only working for operators
        query_str = f"SELECT * FROM {self.selected_table_name} WHERE {column_val} {operation_val}" \
                    f" '{input_val}'"

        treeFunctions.clear_tree(tree_view)

        columns_names = createCsvFromDb.extract_table_column_names(self.selected_table_name)
        treeFunctions.remove_columns(tree_view, columns_names)
        treeFunctions.add_columns(tree_view, columns_names)

        entries = createCsvFromDb.execute_query(query_str)
        for row in entries:
            tree_view.insert("", tk.END, values=row)
        tree_view.update()

        # TODO try catch on this method, this would happen probably on invalid query,
        # TODO get the columns of the query into a list
        # TODO add query_str to table operatrions list
        # TODO add when clicked on table operation list, display the query based on what was saved in output_queries
        # TODO add when right clicked on table operation list, remove query from table list and from output queries

    def refresh(self):
        # Reset var and delete all old options
        self.column_clicked.set('')
        self.column_checkbox['menu'].delete(0, 'end')

        self.operation_clicked.set('')
        self.operation_checkbox['menu'].delete(0, 'end')

    def table_list_select_click(self, event):
        treeFunctions.clear_tree(tree_view)
        treeFunctions.remove_columns(tree_view, tree_view['columns'])

        self.refresh()
        self.selected_table_name = self.table_list.get(self.table_list.curselection())

        self.column_choices = createCsvFromDb.extract_table_column_names(self.selected_table_name)
        self.column_clicked.set(self.column_choices[0])

        for choice in self.column_choices:
            self.column_checkbox['menu'].add_command(label=choice, command=tk._setit(self.column_clicked, choice))

        self.operation_choices = ('>', '<', '=', '>=', '<=',
                                  '!=', 'LIKE', 'IN', 'IS NULL', 'IS NOT NULL')
        self.operation_clicked.set(self.operation_choices[0])

        for choice in self.operation_choices:
            self.operation_checkbox['menu'].add_command(label=choice, command=tk._setit(self.operation_clicked, choice))

        columns_names = createCsvFromDb.extract_table_column_names(self.selected_table_name)
        entries = createCsvFromDb.extract_entries_from_table(self.selected_table_name)

        treeFunctions.add_columns(tree_view, columns_names)
        for row in entries:
            tree_view.insert("", tk.END, values=row)
        tree_view.update()

        cols = tree_view['columns']
        for col in cols:
            tree_view.column(col, width=100, minwidth=110)  # restore to desired size


def populate_listbox(my_list_box, list_entries):
    for i in list_entries:
        my_list_box.insert("end", i)


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
