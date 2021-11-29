def clear_tree(tree):
    for i in tree.get_children():
        tree.delete(i)

def remove_columns(gui ,columns, **kwargs):
    # Preserve current column headers
    current_columns = list(gui.view['columns'])

    # Remove columns
    current_columns = [x for x in current_columns if x not in columns]

    # Preserve current column settings
    current_columns = {key: gui.view.heading(key) for key in current_columns}

    # Update without removed columns
    gui.view['columns'] = list(current_columns.keys()) + list(columns)
    for key in columns:
        gui.view.heading(key, text=key, **kwargs)

    # Set saved column values for the already existing columns
    for key in current_columns:
        # State is not valid to set with heading
        state = current_columns[key].pop('state')
        gui.view.heading(key, **current_columns[key])