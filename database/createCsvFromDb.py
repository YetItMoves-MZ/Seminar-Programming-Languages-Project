import sqlite3
import traceback

import pandas as pd
from IPython.display import display
import sys

conn = None
cur = None

DEFAULT_DATABASE_PATH = 'database/chinook.db'


def csv_from_db_init(db=DEFAULT_DATABASE_PATH):
    global conn, cur
    conn = sqlite3.connect(db)
    cur = conn.cursor()


def csv_from_db_destroy():
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()


def CreateCsvFromDB(db=DEFAULT_DATABASE_PATH):
    print("\n" + db + " db Schema")
    cur.execute( \
        "SELECT name "
        "FROM sqlite_master "
        "WHERE type='table';")
    tables = cur.fetchall()
    print("tables:", tables)

    for column in tables:
        table_name = column[0]
        print("Table Name: ", table_name)
        # display_table(cur, conn, table_name)
        cur.execute("PRAGMA table_info(" + table_name + ")")
        info = cur.fetchall()
        print("   " + table_name + " attributes:")
        for col in info:
            print("   ", col)
        cur.execute("""SELECT * FROM """ + table_name)
        df = pd.DataFrame(cur.fetchall())
        df.columns = [x[0] for x in cur.description]
        # display(df)
        # print(df)
        print("\n")

        table = pd.read_sql_query( \
            "SELECT * from %s" % table_name, conn)
        csvFileName = table_name + '.csv'
        table.to_csv(csvFileName, index_label='index')

    # print("\n")
    # display_table(cur, conn, "genres")
    # cur.close()
    # conn.close()


def left_align(df):
    left_aligned_df = \
        df.style.set_properties(**{'text-align': 'left'})
    left_aligned_df = left_aligned_df.set_table_styles(
        [dict(selector='th',
              props=[('text-align', 'left')])])
    return left_aligned_df


def display_table(cur, conn, tableName):
    cur.execute(f'SELECT * FROM {tableName}')
    results = cur.fetchall()
    print("Table Name: ", tableName)
    table = list(pd.read_sql_query(
        "SELECT * from %s" % tableName, conn))
    col_width = \
        max( \
            len(str(word)) \
            for row in results for word in row) + 2
    for col in table:
        print("".join(col.ljust(col_width)), end='')
    print()
    for row in results:
        # print(row)
        print( \
            "".join(str(word).ljust(col_width) \
                    for word in row))
    print()


def _extract_tables():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    return tables


def extract_max_columns():
    tables = _extract_tables()

    max_num_columns = -1

    # iterate on tables fetching their structure, and comparing max columns
    for table in tables:
        table_name = table[0]
        cur.execute("PRAGMA table_info(" + table_name + ")")
        info = cur.fetchall()
        num_columns = len(info)
        if num_columns > max_num_columns:
            max_num_columns = num_columns

    return max_num_columns


def extract_table_names():
    tables = _extract_tables()
    # table name is the first item in the table
    return [table[0] for table in tables]


def extract_table_column_names(table_name):
    cur.execute("PRAGMA table_info(" + table_name + ")")
    info = cur.fetchall()
    # column name is index number 1 in the column
    return [col[1] for col in info]


def extract_entries_from_table(table_name):
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    return rows


def execute_query(query_str):
    try:
        cur.execute(query_str)
        # conn.commit()
        results = cur.fetchall()
        return results
    except sqlite3.Error as er:
        return f"Query Failed: Error: {str(er)}"


def is_select_match_input(table_name, column_name):
    query_str = "SELECT DATA_TYPE FROM sqlite_master.COLUMNS" \
                f" WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column_name}'"
    cur.execute(query_str)
    result = cur.fetchall()
    return result


def insert_new_table(sql_statement, table_rows):
    # TODO needs implementation
    cur.executemany(sql_statement, table_rows)


def main():
    sys.stdout = open( \
        "database/CreateCsvFromDBoutput.txt", 'w', encoding="utf-8")
    CreateCsvFromDB()
    sys.stdout.close()


if __name__ == '__main__':
    main()
