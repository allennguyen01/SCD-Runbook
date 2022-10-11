# imports for SQL data part
import pyodbc
from datetime import datetime, timedelta
import pandas as pd

# Establish the Python SQL Server Connection
cnxn_str = ("Driver=SQL Server;"
            "Server=VIC1MSDBSTW03;"
            "Database=SCDRunbook;"
            "Trusted_Connection=yes;")

print(cnxn_str)

# initialise connection (assume we have already defined cnxn_str)
cnxn = pyodbc.connect(cnxn_str) 

# build up our query string
query = ("SELECT * FROM ABAT_PATHNAMES")

# execute the query and read to a dataframe in Python
data = pd.read_sql(query, cnxn)

# write out data.
print(data)

del cnxn  # close the connection