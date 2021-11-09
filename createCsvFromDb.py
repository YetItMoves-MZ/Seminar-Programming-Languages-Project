import sqlite3
import pandas as pd
from IPython.display import display
import sys

def CreateCsvFromDB(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print("\n" + db +" db Schema")
    cur.execute(\
        "SELECT name "
        "FROM sqlite_master "
        "WHERE type='table';")
    tables = cur.fetchall()
    print("tables:", tables)

    for column in tables:
      table_name = column[0]
      print("Table Name: ", table_name)
      #display_table(cur, conn, table_name)
      cur.execute("PRAGMA table_info(" + table_name + ")")
      info = cur.fetchall()
      print ("   " + table_name + " attributes:")
      for col in info:
          print("   ", col)
      cur.execute("""SELECT * FROM """ + table_name)
      df = pd.DataFrame(cur.fetchall())
      df.columns = [x[0] for x in cur.description]
      #display(df)
      #print(df)
      print("\n")

      table = pd.read_sql_query(\
            "SELECT * from %s" % table_name, conn)
      csvFileName = table_name + '.csv'
      table.to_csv(csvFileName, index_label='index')

    print("\n")
    display_table(cur, conn, "genres")
    cur.close()
    conn.close()

def left_align(df):
    left_aligned_df = \
        df.style.set_properties(**{'text-align': 'left'})
    left_aligned_df = left_aligned_df.set_table_styles(
        [dict(selector='th',
              props=[('text-align', 'left')])])
    return left_aligned_df

def display_table(cur, conn, tableName):
    cur.execute('SELECT * FROM %s' % tableName)
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

def main():
    sys.stdout = open(\
        "CreateCsvFromDBoutput.txt", 'w', encoding="utf-8")
    CreateCsvFromDB('chinook.db')
    sys.stdout.close()

main()
