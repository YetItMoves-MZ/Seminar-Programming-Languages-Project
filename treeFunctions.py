def clear_tree(tree):
    for i in tree.get_children():
        tree.delete(i)


def remove_columns(tree, columns, **kwargs):
    # Preserve current column headers
    current_columns = list(tree['columns'])

    # Remove columns
    current_columns = [x for x in current_columns if x not in columns]

    # Preserve current column settings
    current_columns = {key: tree.heading(key) for key in current_columns}

    # Update without removed columns
    tree['columns'] = list(current_columns.keys())

    # Set saved column values for the already existing columns
    for key in current_columns:
        # State is not valid to set with heading
        state = current_columns[key].pop('state')
        tree.heading(key, **current_columns[key])


def add_columns(tree, columns, **kwargs):
    # Preserve current column headers and their settings
    current_columns = list(tree['columns'])
    current_columns = {key: tree.heading(key) for key in current_columns}

    # Update with new columns
    tree['columns'] = list(current_columns.keys()) + list(columns)
    for key in columns:
        tree.heading(key, text=key, **kwargs)

    # Set saved column values for the already existing columns
    for key in current_columns:
        # State is not valid to set with heading
        state = current_columns[key].pop('state')
        tree.heading(key, **current_columns[key])
