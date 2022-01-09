import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, END
import database.createCsvFromDb as createCsvFromDb
import treeFunctions
import os

root = None
tree_view = None
tables_list = None
app = None

wrapper1 = None
wrapper2 = None


class App:
    def __init__(self, root):
        """
        __init__(...) initialize the gui
        :param root: the root window
        """
        root.title("Seminar Project")
        width = 900
        height = 520
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(align_str)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times', size=10)

        # display name -> table name -> query str
        self.table_name_to_query_str = {}
        self.display_name_to_table_name = {}

        self.filter_table_name = None
        self.database_table_name = None

        self.table_list_choices = ()
        self.table_list_clicked = tk.StringVar(wrapper2)
        self.table_list_clicked.trace("w", self.select_database_table)
        self.table_list = tk.OptionMenu(wrapper2, self.table_list_clicked, self.table_list_choices)
        self.table_list["font"] = ft
        self.table_list.place(x=5, y=65, width=170, height=30)
        populate_table_list_option_menu(self.table_list, tables_list, self.table_list_clicked)

        self.table_lists_label = tk.Label(wrapper2)
        self.table_lists_label["font"] = ft
        self.table_lists_label["justify"] = "center"
        self.table_lists_label["text"] = "Tables List"
        self.table_lists_label.place(x=0, y=35, width=180, height=30)

        self.table_filter_Label = tk.Label(wrapper2)
        self.table_filter_Label["font"] = ft
        self.table_filter_Label["justify"] = "center"
        self.table_filter_Label["text"] = "Tables Filter"
        self.table_filter_Label.place(x=405, y=35, width=480, height=30)

        self.table_filter_list = tk.Listbox(wrapper2)
        self.table_filter_list["font"] = ft
        self.table_filter_list["justify"] = "center"
        self.table_filter_list.place(x=410, y=65, width=470, height=190)
        self.table_filter_list.bind('<<ListboxSelect>>', self.table_filter_list_select_click)

        self.column_label = tk.Label(wrapper2)
        self.column_label["font"] = ft
        self.column_label["justify"] = "center"
        self.column_label["text"] = "Column"
        self.column_label.place(x=175, y=60, width=100, height=30)

        self.column_choices = ()
        self.column_clicked = tk.StringVar(wrapper2)
        self.column_checkbox = tk.OptionMenu(wrapper2, self.column_clicked, self.column_choices)
        self.column_checkbox["font"] = ft
        self.column_checkbox.place(x=255, y=60, width=130, height=30)

        self.from_label = tk.Label(wrapper2)
        self.from_label["font"] = ft
        self.from_label["justify"] = "center"
        self.from_label["text"] = "From"
        self.from_label.place(x=175, y=95, width=100, height=30)

        self.from_table_text = tk.StringVar()
        self.from_table_text.set("")
        self.from_table_label = tk.Label(wrapper2, textvariable=self.from_table_text)
        self.from_table_label["font"] = ft
        self.from_table_label["justify"] = "center"
        self.from_table_label.place(x=260, y=95, width=100, height=30)

        self.operation_label = tk.Label(wrapper2)
        self.operation_label["font"] = ft
        self.operation_label["justify"] = "center"
        self.operation_label["text"] = "Operation"
        self.operation_label.place(x=175, y=130, width=100, height=30)

        self.operation_choices = ()
        self.operation_clicked = tk.StringVar(wrapper2)
        self.operation_clicked.trace("w", self.select_sql_operation)
        self.operation_checkbox = tk.OptionMenu(wrapper2, self.operation_clicked, self.operation_choices)
        self.operation_checkbox["font"] = ft
        self.operation_checkbox.place(x=255, y=130, width=130, height=30)

        self.value_label = tk.Label(wrapper2)
        self.value_label["font"] = ft
        self.value_label["justify"] = "center"
        self.value_label["text"] = "Value"
        self.value_label.place(x=175, y=180, width=100, height=30)

        self.value_text = tk.Text(wrapper2)
        self.value_text["font"] = ft
        self.value_text.place(x=255, y=180, width=130, height=30)

        self.case_sensitive_label = tk.Label(wrapper2)
        self.case_sensitive_label["font"] = ft
        self.case_sensitive_label["justify"] = "center"
        self.case_sensitive_label["text"] = "Case Sensitive"
        self.case_sensitive_label.place(x=175, y=230, width=100, height=30)

        self.case_sensitive_choice = tk.IntVar()
        self.case_sensitive_checkbox = tk.Checkbutton(wrapper2, variable=self.case_sensitive_choice, onvalue=1,
                                                      offvalue=0)
        self.case_sensitive_checkbox.place(x=270, y=230, width=20, height=30)

        self.add_button = tk.Button(wrapper2)
        self.add_button["font"] = ft
        self.add_button["justify"] = "center"
        self.add_button["text"] = "+"
        self.add_button.place(x=300, y=225, width=30, height=30)
        self.add_button["command"] = self.add_query_to_table_filter_list

        self.remove_button = tk.Button(wrapper2)
        self.remove_button["font"] = ft
        self.remove_button["justify"] = "center"
        self.remove_button["text"] = "-"
        self.remove_button.place(x=345, y=225, width=30, height=30)
        self.remove_button["command"] = self.table_filter_delete_event

        self.execute_button = tk.Button(wrapper2)
        self.execute_button["font"] = ft
        self.execute_button["justify"] = "center"
        self.execute_button["text"] = "Execute"
        self.execute_button.place(x=255, y=270, width=130, height=25)
        self.execute_button["command"] = self.execute_query

        self.error_message_text = tk.Text(wrapper2)
        self.error_message_text["font"] = ft
        self.error_message_text.place(x=410, y=270, width=470, height=35)

        self.init_operations()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_operations(self):
        """
        init_operations(...) initialize operations and sets them into the checkbox
        :return: None
        """
        self.operation_choices = ('>', '<', '=', '>=', '<=',
                                  '!=', 'LIKE', 'IN', 'IS NULL', 'IS NOT NULL')

        self.operation_clicked.set(self.operation_choices[0])
        for choice in self.operation_choices:
            self.operation_checkbox['menu'].add_command(label=choice,
                                                        command=tk._setit(self.operation_clicked, choice))

    def delete_filter_table(self, displayed_table_name):
        """
        delete_filter_table(...) deletes a selected table
        :param displayed_table_name: a table name to delete
        :return: None
        """
        for all_displayed_table_name in self.display_name_to_table_name:
            table_name = self.display_name_to_table_name[all_displayed_table_name]
            createCsvFromDb.drop_table(table_name)

            csv_file_name = f"{table_name}.csv"
            if os.path.exists(csv_file_name):
                os.remove(csv_file_name)
        table_name = self.display_name_to_table_name[displayed_table_name]
        del self.table_name_to_query_str[table_name]
        del self.display_name_to_table_name[displayed_table_name]
        self.filter_table_name = None

    def table_filter_delete_event(self):
        """
        table_filter_delete_event(...) deletes a selected new table
        :return: None
        """
        if not validate_my_event(self.table_filter_list):
            return

        selected_idx = self.table_filter_list.curselection()
        displayed_table_name = self.table_filter_list.get(selected_idx)
        self.table_filter_list.delete(selected_idx)

        self.delete_filter_table(displayed_table_name)

    def query_builder(self, column_val, operation_val, input_val):
        """
        query_builder(...) builds a query string from input
        :param column_val: column name
        :param operation_val: operation name
        :param input_val: the input for the given query
        :return: query string
        """
        # extract information for building query
        case_sensitive_val = self.case_sensitive_choice.get()

        is_null_operation = True if operation_val in ['IS NULL', 'IS NOT NULL'] else False
        is_multi_variable = True if ',' in input_val else False
        is_in_operation = True if operation_val in ['IN'] else False

        # if operation is null/ is not null
        if is_null_operation:
            query_str = f"WHERE {column_val} {operation_val}"

        elif is_in_operation:
            if not is_multi_variable:
                query_str = f"WHERE {column_val} {operation_val} ('{input_val}')"
            else:
                input_val = tuple(input_val.split(","))
                input_val = f"{input_val}".replace(" ", "")
                query_str = f"WHERE {column_val} {operation_val} {input_val}"

        # single value
        else:
            query_str = f"WHERE {column_val} {operation_val} '{input_val}'"

        # case sensitive
        createCsvFromDb.execute_query(f"PRAGMA case_sensitive_like = {case_sensitive_val};")
        if not case_sensitive_val and not is_null_operation:
            query_str += " COLLATE NOCASE"
        return query_str

    def validate_query_is_new(self, new_table_name):
        """
        validate_query_is_new(...) checks if the given name already exists
        :param new_table_name: newly created table name
        :return: boolean answer
        """
        self.error_message_text.delete('1.0', END)
        if new_table_name in self.table_name_to_query_str:
            self.error_message_text.insert(END, f"{new_table_name} already exist")
            return False

        return True

    def create_new_table_name(self):
        """
        create_new_table_name: create table name from gui elements
        :return: new table name
        """
        column_val = self.column_clicked.get()
        operation_val = self.operation_clicked.get()
        input_val = self.value_text.get("1.0", "end-1c")

        operation_str = translate_operator_to_word(operation_val)
        input_str = translate_input_to_word(input_val)
        new_table_name = f"{column_val}_{operation_str}_{input_str}"

        return new_table_name

    def add_query_to_table_filter_list(self):
        """
        add_query_to_table_filter_list(...) add the query to filter table
        :return: None
        """
        if self.database_table_name == "" or self.database_table_name is None:
            return

        column_val = self.column_clicked.get()
        operation_val = self.operation_clicked.get()
        input_val = self.value_text.get("1.0", "end-1c")

        is_null_operation = True if operation_val in ['IS NULL', 'IS NOT NULL'] else False
        if not is_null_operation and input_val == "":
            self.error_message_text.delete("1.0", tk.END)
            self.error_message_text.insert(tk.END, "no value was given")
            return

        new_table_name = self.create_new_table_name()

        if not self.validate_query_is_new(new_table_name):
            return

        query_str = self.query_builder(column_val, operation_val, input_val)

        new_query_name = f"{column_val} {operation_val} {input_val}"
        self.display_name_to_table_name[new_query_name] = new_table_name
        self.table_name_to_query_str[new_table_name] = query_str
        self.table_filter_list.insert("end", new_query_name)

    def execute_query(self):
        """
        execute_query(...) creates and execute a query
        :return: None
        """
        # delete previews error
        self.error_message_text.delete("1.0", tk.END)

        previews_table_name = ""
        for display_name in self.display_name_to_table_name:
            if previews_table_name == "":
                previews_table_name = self.database_table_name

            new_table_name = self.display_name_to_table_name[display_name]
            query_str = self.table_name_to_query_str[new_table_name]
            query_str = f"SELECT * FROM {previews_table_name} {query_str}"

            # create new table and return its entries
            entries = self.create_new_table_from_query(query_str, new_table_name)
            if isinstance(entries, str):
                error_str = entries
                self.error_message_text.insert(END, error_str)
                return
            previews_table_name = self.display_name_to_table_name[display_name]

        # check if dictionary is empty
        if self.table_filter_list.get(0):
            update_tree_view(entries, new_table_name)

    def create_new_table_from_query(self, query_str, table_name):
        """
        create_new_table_from_query(...) creates a new table
        :param query_str: the given query
        :param table_name: the new table name
        :return: list of rows if there is no error or an error message if an error was found
        """
        error = createCsvFromDb.insert_new_table(table_name, query_str)

        # if error is not str, no error happened
        if isinstance(error, str):
            error_lower = error.lower()
            if "query failed" not in error_lower or "already exist" not in error_lower:
                return error
        entries = createCsvFromDb.execute_query(f"SELECT * FROM {table_name}")

        # if error is not str, no error happened
        if isinstance(entries, str):
            error_str = entries
            self.error_message_text.insert(END, error_str)
            return error

        return entries

    def get_error_message_text(self):
        """
        get_error_message_text(...) getter
        :return: the error message text
        """
        return self.error_message_text

    def refresh(self):
        """
        refresh(...) resets the gui
        :return: None
        """
        # Reset var and delete all old options
        self.column_clicked.set('')
        self.column_checkbox['menu'].delete(0, 'end')

        self.operation_clicked.set('')

    def select_table_event(self, table_name):
        """
        select_table_event(...)  sets the view according to the selected table
        :param table_name: the name of the selected table
        :return: None
        """
        treeFunctions.clear_tree(tree_view)
        treeFunctions.remove_columns(tree_view, tree_view['columns'])

        self.refresh()
        self.database_table_name = table_name

        self.column_choices = createCsvFromDb.extract_table_column_names(self.database_table_name)
        self.column_clicked.set(self.column_choices[0])

        for choice in self.column_choices:
            self.column_checkbox['menu'].add_command(label=choice, command=tk._setit(self.column_clicked, choice))

        self.from_table_text.set(self.database_table_name)

        entries = createCsvFromDb.extract_entries_from_table(self.database_table_name)

        update_tree_view(entries, self.database_table_name)

    def table_filter_list_select_click(self, event):
        """
        table_filter_list_select_click(...) on a given event: if the event is valid, then save the table name that was
        selected from the table filter listbox and update the tree view
        :param event: the given event
        :return: None
        """
        if not validate_my_event(self.table_filter_list):
            return
        table_name = self.table_filter_list.get(self.table_filter_list.curselection())
        self.filter_table_name = table_name

    def select_database_table(self, *args):
        """
        option_changed(...) table_list_clicked (OptionMenu) change event
        :return: None
        """
        table_name = self.table_list_clicked.get()
        if len(table_name) != 0:
            self.table_list_clicked.set(f'{table_name}')
            self.select_table_event(table_name)

    def select_sql_operation(self, *args):
        """
        select_sql_operation(...) operation_checkbox (OptionMenu) change event
        :return: None
        """
        operation_name = self.operation_clicked.get()
        self.value_text.delete('1.0', tk.END)
        null_operation = ['IS NULL', 'IS NOT NULL']
        if len(operation_name) != 0 and operation_name in null_operation:
            self.value_text.configure(state=tk.DISABLED)
        else:
            self.value_text.configure(state=tk.NORMAL)

    def on_closing(self):
        """
        on_closing(...) deleting all newly created tables and closing the database and gui
        :return: None
        """

        self.delete_all_filter_tables()
        root.destroy()

    def delete_all_filter_tables(self):
        """
        delete_all_filter_tables(...) deleting all filter tables
        :return: None
        """
        temp = self.display_name_to_table_name.copy()
        for displayed_table_name in temp.keys():
            self.delete_filter_table(displayed_table_name)
        temp.clear()


def validate_my_event(list_widget):
    """
    validate_my_event(...) validates that a table was selected from the listbox
    :param list_widget: the list widget
    :return: boolean answer
    """

    selection = list_widget.curselection()
    return len(selection) != 0


def update_tree_view(entries, table_name):
    """
    update_tree_view(...) updates the tree view after a query
    :param entries: a list of rows after the query
    :param table_name: the name of the old table
    :return: None
    """
    treeFunctions.clear_tree(tree_view)
    columns_names = createCsvFromDb.extract_table_column_names(table_name)
    treeFunctions.remove_columns(tree_view, columns_names)
    treeFunctions.add_columns(tree_view, columns_names)

    for row in entries:
        tree_view.insert("", tk.END, values=row)
    tree_view.update()

    cols = tree_view['columns']
    reverse = 1
    for col in cols:
        tree_view.column(col, width=100, minwidth=110)  # restore to desired size
        tree_view.heading(column=col, text=col, anchor='w',
                          command=lambda _col=col: tree_view_sort_column(tree_view, _col, not reverse))


def translate_operator_to_word(operator):
    """
    translate_operator_to_word(...) translates the given operators to words
    :param operator: the operator we want to translate into words
    :return: a string consists of words that explains the operator
    """
    if operator == ">":
        return "bigger_than"
    elif operator == "<":
        return "smaller_than"
    elif operator == "=":
        return "equal"
    elif operator == "!=":
        return "not_equal"
    elif operator == "<=":
        return "smaller_or_equal"
    elif operator == ">=":
        return "bigger_or_equal"
    else:
        return operator.lower().replace(" ", "_")


def translate_word_to_operator(words):
    """
    translate_word_to_operator(...) translates the given word to operator
    :param words: the words we want to translate into operator
    :return: string operator
    """
    if words == "bigger_than":
        return ">"
    elif words == "smaller_than":
        return "<"
    elif words == "equal":
        return "="
    elif words == "not_equal":
        return "!="
    elif words == "smaller_or_equal":
        return "<="
    elif words == "bigger_or_equal":
        return ">="
    else:
        return words.Upper().replace("_", " ")


def translate_input_to_word(input):
    """
    translate_input_to_word(...) create a valid string for table name from input
    :param input: a string that may contain invalid chars
    :return: a string that does not contain any invalid chars
    """
    rv = input
    invalids_chars = ["%", "'", "*", "||", "-", "*", "/", "<>", "<", ">", ",", "=", " ", "<=", ">=", "~=", "!=",
                      "^=", "(", ")", ":"]
    for invalid_char in invalids_chars:
        rv = rv.replace(invalid_char, "_")

    return rv


def contains_digit(string):
    """
    contains_digit(...) check if a string contains a digit
    :param string: the string we want to check
    :return: boolean answer
    """
    for character in string:
        if character.isdigit():
            return True
    return False


def tree_view_sort_column(treeview: ttk.Treeview, col, reverse: bool):
    """
    tree_view_sort_column(...) sort the table by column when clicking in column
    :param treeview: the treeview
    :param col: the clicked column
    :param reverse: reverse sort or normal sort
    :return: None
    """
    try:
        data_list = [
            (int(treeview.set(k, col)), k) for k in treeview.get_children("")
        ]
    except Exception:
        data_list = [(treeview.set(k, col), k) for k in treeview.get_children("")]

    data_list.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(data_list):
        treeview.move(k, "", index)

    tree_view.heading(column=col, text=col, anchor='w',
                      command=lambda _col=col: tree_view_sort_column(tree_view, col, not reverse))


def populate_table_list_option_menu(my_option_menu, list_entries, table_list_clicked):
    """
    populate_table_list_option_menu(...) populates the given OptionMenu from a given list of entries
    :param my_option_menu: the OptionMenu we want to populate
    :param list_entries: the list of entries
    :param table_list_clicked: provides helper functions for directly creating and accessing variables
    :return: None
    """

    for choice in list_entries:
        my_option_menu['menu'].add_command(label=choice, command=tk._setit(table_list_clicked, choice))


def configure_scrollbars():
    """
    configure_scrollbars(...) configure and sets the scrollbars
    :return: None
    """
    x_scrollbar = tk.Scrollbar(wrapper1, orient=tk.HORIZONTAL)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    y_scrollbar = tk.Scrollbar(wrapper1, orient=tk.VERTICAL, command=tree_view.yview())
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree_view.configure(yscrollcommand=y_scrollbar.set)
    tree_view.configure(xscrollcommand=x_scrollbar.set)
    tree_view.pack()

    for col in tree_view['columns']:
        tree_view.heading(col, text=f"{col}", anchor='w')
        tree_view.column(col, anchor='w', width=40)  # initially smaller size
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

    wrapper2 = tk.LabelFrame(root, text="")
    wrapper2.pack(side=tk.BOTTOM, fill="both", padx=0, pady=0)
    wrapper2.place(x=0, y=200, width=900, height=320)
    app = App(root)
    wrapper1 = tk.LabelFrame(root, text="")
    wrapper1.pack(side=tk.TOP, fill="both", padx=0, pady=0)
    wrapper1.place(x=0, y=0, width=900, height=200)
    tree_view = ttk.Treeview(wrapper1, columns=(), show='headings', selectmode='extended')
    configure_scrollbars()

    treeFunctions.add_columns(tree_view, columns)
    root.mainloop()
