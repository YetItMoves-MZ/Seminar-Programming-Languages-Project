import tkinter as tk

class GUI:
    def __init__(self, master):
        self.view = tk.ttk.Treeview(master)
        self.view.pack()
        self.view.heading('#0', text='Name')

        self.view.insert('', 'end', text='Foo')
        self.view.insert('', 'end', text='Bar')
        self.view['columns'] = ('foo')
        self.view.heading('foo', text='foo')
        self.view.set(self.view.get_children()[0], 'foo', 'test')
        self.add_columns(('bar', 'blesh'))

    def add_columns(self, columns, **kwargs):
        # Preserve current column headers and their settings
        current_columns = list(self.view['columns'])
        current_columns = {key: self.view.heading(key) for key in current_columns}

        # Update with new columns
        self.view['columns'] = list(current_columns.keys()) + list(columns)
        for key in columns:
            self.view.heading(key, text=key, **kwargs)

        # Set saved column values for the already existing columns
        for key in current_columns:
            # State is not valid to set with heading
            state = current_columns[key].pop('state')
            self.view.heading(key, **current_columns[key])

    def remove_columns(self, columns, **kwargs):
        # Preserve current column headers and their settings
        current_columns = list(self.view['columns'])
        current_columns = {key: self.view.heading(key) for key in current_columns}


