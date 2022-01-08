import sqlite3

import pandas as pd
import sys

conn = None
cur = None

DEFAULT_DATABASE_PATH = 'database/chinook.db'


def csv_from_db_init(db=DEFAULT_DATABASE_PATH):
    """
    csv_from_db_init(...) initialize the database
    :param db: the given database
    :return: None
    """
    global conn, cur
    conn = sqlite3.connect(db)
    cur = conn.cursor()


def csv_from_db_destroy():
    """
    csv_from_db_destroy(...) close the database connection
    :return: None
    """
    global conn, cur
    if conn is not None:
        conn.close()
        conn = None
    if cur is not None:
        cur.close()
        cur = None


def create_csv_from_db(db=DEFAULT_DATABASE_PATH):
    """
    create_csv_from_db(...) creates a new csv from database
    :param db: the database
    :return: None
    """
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
        cur.execute("PRAGMA table_info(" + table_name + ")")
        info = cur.fetchall()
        print("   " + table_name + " attributes:")
        for col in info:
            print("   ", col)
        cur.execute("""SELECT * FROM """ + table_name)
        df = pd.DataFrame(cur.fetchall())
        df.columns = [x[0] for x in cur.description]
        print("\n")

        table = pd.read_sql_query( \
            "SELECT * from %s" % table_name, conn)
        csv_file_name = table_name + '.csv'
        table.to_csv(csv_file_name, index_label='index')


def _extract_tables():
    """
    _extract_tables(...) extracts all tables from the database
    :return: all tables as a list
    """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    return tables


def extract_max_columns():
    """
    extract_max_columns(...) extracts the highest number of columns in any table from all tables in the database
    :return: integer maximum number of columns
    """
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
    """
    extract_table_names(...) extracts the table names of all tables in the database
    :return: a list of table names
    """
    tables = _extract_tables()
    # table name is the first item in the table
    return [table[0] for table in tables]


def extract_table_column_names(table_name):
    """
    extract_table_column_names(...) extracts all the names of the columns of a given table
    :param table_name: a string table name
    :return: a list of column names
    """
    cur.execute("PRAGMA table_info(" + table_name + ")")
    info = cur.fetchall()
    # column name is index number 1 in the column
    return [col[1] for col in info]


def extract_entries_from_table(table_name):
    """
    extract_entries_from_table(...) extracts all rows from a given table
    :param table_name: string table name
    :return: a list of rows
    """
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    return rows


def execute_query(query_str):
    """
    execute_query(...) execute a given query
    :param query_str: a string of the given query
    :return: the result if the query succeed or an error message if it didn't
    """
    try:
        cur.execute(query_str)
        # conn.commit()
        results = cur.fetchall()
        return results
    except sqlite3.Error as er:
        return f"Query Failed: Error: {str(er)}"


def insert_new_table(new_table_name, query_str):
    """
    insert_new_table(...) creates a new table
    :param new_table_name: the name of the table we want to create
    :param query_str: the query that is used on the table
    :return: result of the execute
    """
    create_query = f"CREATE TABLE {new_table_name} AS {query_str}"
    return execute_query(create_query)


def drop_table(table_name):
    """
    drop_table(...) destroy a table
    :param table_name: string name of the table
    :return: the result of the execute
    """
    query = f"DROP TABLE {table_name}"
    return execute_query(query)


def main(stdout_file="database/CreateCsvFromDBoutput.txt", database_name="database/chinook.db"):
    sys.stdout = open(stdout_file, 'w', encoding="utf-8")
    csv_from_db_init(database_name)

    drop_table('__5')
    create_csv_from_db()
    sys.stdout.close()


if __name__ == '__main__':
    main("CreateCsvFromDBoutput.txt", "chinook.db")
