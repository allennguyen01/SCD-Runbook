# imports for SQL data part
import pyodbc
from datetime import datetime, timedelta
import pandas as pd

def read_sql(SQL_query):
    # Establish the Python SQL Server Connection
    cnxn_str = ("Driver=SQL Server;"
                "Server=VIC1MSDBSTW03;"
                "Database=SCDRunbook;"
                "Trusted_Connection=yes;")

    # Initialise connection (assume we have already defined cnxn_str)
    cnxn = pyodbc.connect(cnxn_str) 

    # Read SQL file and convert to a string
    with open(SQL_query, 'r') as sqlfile:
        queryString = sqlfile.read()

    # Execute the query and read to a dataframe in Python
    data = pd.read_sql(queryString, cnxn)

    # Close the connection
    del cnxn  

    # Return SQL result as Pandas dataframe
    return data

def main():
    print(read_sql('runbook_test.sql'))

if __name__ == '__main__':
    main()