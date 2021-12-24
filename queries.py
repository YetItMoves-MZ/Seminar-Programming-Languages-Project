import sqlite3
import pandas as pd
from IPython.display import display
from sqlalchemy import create_engine
import sys

def Queries(db):
  try:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    engine = create_engine('sqlite:///' + db)

    Q0 = """
    SELECT invoice_."BillingCountry" AS "Country"
    FROM invoices AS invoice_
    WHERE invoice_."BillingCountry" 
          IN ('USA', 'United Kingdom', 'Canada')
    GROUP BY 1
    ORDER BY 1 DESC"""
    print("\nQ0: " + Q0 + "\n")
    execute_query(Q0, cur, conn, engine)

    Q1 = """
      SELECT CAST(strftime('%Y', invoice_."InvoiceDate") AS BIGINT) 
        AS "Year",
        ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'USA'
          THEN invoice_."Total" END), 2) AS "USA",
        ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'United Kingdom'
          THEN invoice_."Total" END), 2) AS "United Kingdom",
        ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'Canada'
          THEN invoice_."Total" END), 2) AS "Canada"
      FROM invoices AS invoice_
      WHERE invoice_."BillingCountry" IN 
           ('USA', 'United Kingdom', 'Canada')
      GROUP BY 1
      ORDER BY 1 DESC"""
    print("\nQ1: " + Q1 + "\n")
    execute_query(Q1, cur, conn, engine)

    Q2 = """
      SELECT FirstName||" "||LastName as "Customers From Brazil"
      FROM Customers
      WHERE Country = "Brazil";"""
    print("\nQ2: -- Provide a query only showing the Customers " +
          "from Brazil.\n" + Q2 + "\n")
    execute_query(Q2, cur, conn, engine)

    Q3 = """
    SELECT c.FirstName||" "||c.LastName as "Customers", 
           i.InvoiceId,i.InvoiceDate,i.BillingCountry
    FROM Customers c
    LEFT JOIN Invoices i
    ON i.CustomerId = c.CustomerId
    WHERE c.Country = "Brazil";"""
    print("\nQ3: -- Provide a query showing the Invoices "
          +"of customers who are from Brazil. "
          + "\n       The resultant table should show "
          + "the customer's full name, Invoice ID,\n"
          + "       Date of the invoice and billing country.\n"
          + Q3 + "\n")
    execute_query(Q3, cur, conn, engine)

    Q4 = """
    SELECT BillingCountry, COUNT(InvoiceId)
    FROM Invoices
    GROUP BY BillingCountry;"""
    print("\nQ4: -- Provide a query that shows the number\n"
          + "      of invoices per country, using: GROUP BY\n"
          + Q4 + "\n")
    execute_query(Q4, cur, conn, engine)

    Q5 = """
    SELECT COUNT(InvoiceLineId) as "Number Of Line Items"
    FROM Invoice_items 
    WHERE InvoiceId = 37;"""
    print("\nQ5: -- Looking at the InvoiceLine table, provide\n"
          + "       a query  that COUNTs the number of line items\n"
          + "       for Invoice ID 37.\n"
          + Q5 + "\n")
    execute_query(Q5, cur, conn, engine)

    Q6 = """
    SELECT  c.FirstName||" "||c.LastName as "Customer", 
            i.BillingCountry, e.FirstName||" "||e.LastName 
            as "Sale Agent", i.Total
    FROM Invoices i
    JOIN Customers c
    ON c.CustomerId = i.CustomerId
    JOIN Employees e
    ON e.EmployeeId = c.SupportRepId;"""
    print("\nQ6: -- Provide a query that shows the Invoice Total,\n"
           +"       Customer name, Country and Sale Agent name\n"
           +"       for all invoices and customers.\n"
           + Q6 + "\n")
    execute_query(Q6, cur, conn, engine)

    Q7 = """
    SELECT i.InvoiceId, COUNT(il.InvoiceLineId)
           as "Number of invoice lines "
    FROM Invoices i
    JOIN Invoice_items il
    ON i.InvoiceId = il.InvoiceId
    GROUP BY i.InvoiceId;"""
    print("\nQ7: -- Provide a query that shows all Invoices\n"
          + " but includes the number of invoice line items.\n"
          + Q7 + "\n")
    execute_query(Q7, cur, conn, engine)

    Q8 = """
    SELECT a.Title as "Album", mt.Name as "Media type", 
           g.Name as "Genre"
    FROM Tracks t
    JOIN Albums a 
    ON a.AlbumId = t.AlbumId
    JOIN Media_types mt 
    ON mt.MediaTypeId = t.MediaTypeId
    JOIN Genres g
    ON t.GenreId = g.GenreId
    GROUP BY a.Title;"""
    print("\nQ8: -- Provide a query that shows all the Tracks,\n"
      + "       but displays no IDs. The result should include\n"
      + "       the Album name, Media type and Genre.\n" + Q8 + "\n")
    execute_query(Q8, cur, conn, engine)

    Q9 = """
    SELECT COUNT(InvoiceId) as "Total Invoices"
    FROM Invoices
    WHERE InvoiceDate between "2009-01-01" AND "2011-01-01";"""
    print("\nQ9: -- How many Invoices were there in 2009 and 2011?\n"
           + "\n" + Q9 + "\n")
    execute_query(Q9, cur, conn, engine)

    Q10 = """
    SELECT "Media Type" as "Top Media Type", 
           MAX("Times Purchased") as "Times Purchased"
    FROM 
    (SELECT m.Name as "Media type" , 
            COUNT (il.Quantity) as "Times Purchased"
     FROM Invoice_items il
     JOIN Tracks t
     ON il.TrackId = t.Trackid
     JOIN media_types m
     ON m.MediaTypeId = t.MediaTypeId
     GROUP BY m.Name);"""
    print("\nQ10: -- Provide a query that shows the most\n"
          + "        purchased Media Type.\n"
          + "\n" + Q10 + "\n")
    execute_query(Q10, cur, conn, engine)

    Q11 = """
    SELECT p.Name, COUNT(pt.TrackId) as "Number Of Tracks"
    FROM Playlists p
    JOIN Playlist_track pt
    ON p.PlaylistId = pt.PlaylistId
    GROUP BY p.name;"""
    print("\nQ11: -- Provide a query that shows the total number \n"
           + "       of tracks in each playlist.\n"
           + "       The Playlist name should be included\n"
           + "       on the resultant table."
          + "\n" + Q11 + "\n")
    execute_query(Q11, cur, conn, engine)

    Q12 = """
    SELECT e.FirstName||" "||e.LastName as "Sales Agent", 
       COUNT(c.SupportRepId) as "Customer Count"
    FROM Employees e
    JOIN Customers c
    ON c.SupportRepId = e.EmployeeId
    GROUP BY e.EmployeeId;"""
    print(
        "\nQ12: -- Provide a query that shows the count of customers\n"
          + "      assigned to each sales agent.\n"
          + "\n" + Q12 + "\n")
    execute_query(Q12, cur, conn, engine)

    Q13 = """
    SELECT InvoiceLineId, t.Name as "Song", 
           ar.Name as "Artist"
    FROM Invoice_items i 
    JOIN Tracks t
    ON t.TrackId = i.TrackId
    JOIN Albums a 
    ON a.AlbumId = t.AlbumId
    JOIN Artists ar 
    ON ar.ArtistId = a.ArtistId
    WHERE i.TrackId < 10
    ORDER BY t.TrackId;"""
    print("\nQ13: -- Provide a query that includes\n"
           + "       the purchased track name AND artist name\n"
           + "       with each invoice line item.\n"
           + "       (for reduce the output:\n"
           + "          WHERE i.TrackId < 10 was added)."
           + "\n" + Q13 + "\n")
    execute_query(Q13, cur, conn, engine)

    print(
        "\nQ14 + Q15 + Q16:\n"
        + " -- What are the respective total sales\n"
        + "    for each of those years? (2009,2010,2011)\n")

    Q14 = """
    SELECT SUM(Total) as "Total Sales"
    FROM invoices
    WHERE InvoiceDate 
            between "2009-01-01" AND "2010-01-01";"""
    print(Q14)
    execute_query(Q14, cur, conn, engine)

    Q15 = """
    SELECT SUM(Total) as "Total Sales"
    FROM invoices
    WHERE InvoiceDate 
            between "2010-01-01" AND "2011-01-01";"""
    print(Q15)
    execute_query(Q15, cur, conn, engine)

    Q16 = """
    SELECT SUM(Total) as "Total Sales"
    FROM invoices
    WHERE InvoiceDate 
            between "2011-01-01" AND "2012-01-01";"""
    print(Q16)
    execute_query(Q16, cur, conn, engine)

    cur.close()
    conn.close()

  except   UnicodeEncodeError as e:
    return

def execute_query(Q, cur, conn, engine):
    cur.execute(Q)
    results = cur.fetchall()

    df = pd.DataFrame(results)
    df.columns = [x[0] for x in cur.description]
    #print(df.columns)
    display(df)
    # print(df)
    print("\n")

    # same results
    #df = pd.read_sql_query(Q, conn)
    #display(df)

    #display_results(results, Q, cur, conn, engine)
    display_with_engine(results, Q, cur, conn, engine)

def display_results(results, Q, cur, conn, engine):
    table = list(pd.read_sql_query(Q, conn))
    col_width = \
        max( \
            len(str(word)) \
            for row in results for word in row) + 15
    for col in table:
        print("".join(col.ljust(col_width)), end='')
    print()
    for row in results:
        print( \
            "".join(str(word).ljust(col_width) \
                    for word in row))

def display_with_engine(results, Q, cur, conn, engine):
   df = pd.DataFrame(results)
   df.columns = [x[0] for x in cur.description]
   print(list(df.columns))
   rs = engine.execute(Q)
   n = 0
   for row in rs:
     if n < 10:
         print(row)
         n += 1
     else:
         break

def main():
    sys.stdout = open("database/queriesOutput.txt", 'w', encoding="utf-8")
    Queries('chinook.db')
    sys.stdout.close()
