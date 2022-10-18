from unicodedata import name
from sql_to_dataframe import sql_to_dataframe
from df_to_HTML import df_to_HTMLTable
import sys
import pandas as pd
from flask import Flask, render_template, url_for, redirect

# sys.path.append('C:\\Users\\alnguyen\\OneDrive - BCI\\XML Batch Problem\\ActiveBatch_Runbook\\sql_to_dataframe.py')
# import sql_to_dataframe

app = Flask(__name__)

def create_table_template(sqlPath, outHTMLPath):
    df = sql_to_dataframe(sqlPath)

    # Inserted into page_template 
    tableHTML = df_to_HTMLTable(df)

    page_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title></title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <!-- Add jQuery and DataTables library -->
            <script src="jquery-3.6.1.js"></script>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.css">
            <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.js"></script>

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <!-- <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script> -->

            <script>
            $(document).ready( function () {
                $('#table_id').DataTable();
            } );
            </script>
        </head>
    <body>

        %(tableHTML)s

    </body>
    </html>
    """

    with open(outHTMLPath, 'w') as f:
        f.write(page_template % vars())

    for row in df:
        name = row['NAME']
        with open(f"DataTables_Website\plan_pages\{name}.html") as f:
            f.write(f"<h1>{name}</h1>")

if __name__ == '__main__':
    @app.route("/")
    def home():
        return render_template('index.html')

    @app.route("/<name>")
    def plan(name):
        return render_template('plan.html', name=name)

    if __name__ == '__main__':
        app.run(debug=True)

    # create_table_template('DataTables_Website\SCHEDULED_PLANS_FIXED.sql', r'DataTables_Website\templates\index.txt')