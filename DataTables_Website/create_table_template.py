from unicodedata import name
from sql_to_dataframe import sql_to_dataframe
from df_to_HTML import df_to_HTMLTable
import sys
import pandas as pd
from flask import Flask, render_template, url_for, redirect

page_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>%(pageTitle)s</title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link rel="stylesheet" href="styles.css">

            <!-- Add jQuery and DataTables library and Bootstrap 5 integration -->
            <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.1.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.12.1/js/dataTables.bootstrap5.min.js"></script>
            <!-- <script src="..\DataTables_Website\webpages\jquery-3.6.1.js"></script> -->
            <!-- <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.css"> -->

            <!-- CSS library files needed for searchPane filter extension -->
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.2.0/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/dataTables.bootstrap5.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/searchpanes/2.0.2/css/searchPanes.bootstrap5.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/select/1.4.0/css/select.bootstrap5.min.css">

            <!-- JavaScript files needed for searchPane filter extension -->
            <script type="text/javascript" src="https://cdn.datatables.net/searchpanes/2.0.2/js/dataTables.searchPanes.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/searchpanes/2.0.2/js/searchPanes.bootstrap5.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/select/1.4.0/js/dataTables.select.min.js"></script>

            <!-- CSS library files needed for export buttons feature -->
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.dataTables.min.css"/>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.bootstrap5.min.css"/>

            <!-- JavaScript files needed for buttons feature -->
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.bootstrap5.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.html5.min.js"></script>
                <!-- For Excel export button  -->
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/2.5.0/jszip.min.js"></script>
                <!-- For PDF export button -->
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/pdfmake.min.js"></script>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/vfs_fonts.js"></script>
                <!-- For column visibility -->
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.colVis.min.js"></script>

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css">

            <script>
            $(document).ready(function() {
                var table = $('#table_id').DataTable({
                    searchPanes: true,
                    buttons: [
                        {
                            extend: 'excel',
                            text: 'Export as Excel',
                        },
                        {
                            extend: 'pdf',
                            text: 'Export as PDF',
                        },
                        {
                            extend: 'copy',
                            text: 'Copy to clipboard',
                        },
                        {
                            extend: 'collection',
                            text: 'Show/hide columns',
                            buttons: [ 'columnsVisibility' ],
                            visibility: false
                        }
                    ]
                });
                table.searchPanes.container().prependTo(table.table().container());
                table.searchPanes.resizePanes();
                table.buttons().container().prependTo(table.table().container());
            });
            </script>

            <script src="navbar.js"></script>
        </head>
    <body>

    <div class="container-fluid">
        <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
            <a href="index.html" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                <img class="me-4" src="\images\BCI-logo-250x129.png" alt="BCI" height="32px">
                <span class="fs-4">SCD Runbook</span>
            </a>
    
            <ul class="nav nav-pills">
                <li class="nav-item">
                    <button type="button" class="btn btn-light mx-2">
                        <a href="index.html" class="nav-link" id="home-nav-a" onclick="addClassToActivePage()">
                            Scheduled Plans
                        </a>
                    </button>
                    
                </li>
                <li class="nav-item">
                    <button type="button" class="btn btn-light mx-2">
                        <a href="imports.html" class="nav-link" id="imports-nav-a" onclick="addClassToActivePage()">
                            SCD Imports
                        </a>
                    </button>
                </li>
                <li class="nav-item">
                    <button type="button" class="btn btn-light mx-2">
                        <a href="exports.html" class="nav-link" id="exports-nav-a" onclick="addClassToActivePage()">
                            SCD Exports
                        </a>
                    </button>
                </li>
            </ul>
        </header>
    </div>

    <div class="p-4 mb-4 bg-light rounded-3">
        <div class="container-fluid py-2">
            <h1 class="display-5 fw-bold"> %(pageTitle)s </h1>
            <p class="col-md-8 fs-4">If description or documentation available show here.</p>
            <button class="btn btn-primary btn-lg" type="button">Example button</button>
        </div>
    </div>

        <div class="container-fluid">
            %(bodyContent)s
        </div>

    </body>
    </html>
    """

def create_table_template(sqlPath, outHTMLPath):
    df = sql_to_dataframe(sqlPath)

    # Inserted into page_template 
    tableHTML = df_to_HTMLTable(df)

    bodyContent = tableHTML
    pageTitle = 'Page Title' 

    with open(outHTMLPath, 'w') as f:
        f.write(page_template % vars())

def create_plan_pages(sqlPath, SCDConfigSQLPath):
    planDF = sql_to_dataframe(sqlPath)

    plan_template = """
        <h1>%(name)s</h1>

        <h2>Schedule</h2>

        <h2>SCD Batch Job Group Execution</h2>
        %(bjgTableHTML)s

    """
    configDF = sql_to_dataframe(SCDConfigSQLPath)

    for i in range(len(planDF)):
        row = planDF.iloc[i]
        name = row['Name']

        planConfigDF = configDF.loc[configDF['Batch Job Group'] == name]
        bjgTableHTML = df_to_HTMLTable(planConfigDF)

        bodyContent = plan_template % vars()
        pageTitle = name
        
        with open(f"DataTables_Website\webpages\plan_pages\{name}.html", 'w') as f:
            f.write(page_template % vars())

if __name__ == '__main__':
    # create_table_template('DataTables_Website\SQL_queries\SCHEDULED_PLANS.sql', 'DataTables_Website\webpages\index.html')
    # create_table_template('DataTables_Website\SQL_queries\IMPORTS.sql', 'DataTables_Website\webpages\imports.html')
    # create_table_template('DataTables_Website\SQL_queries\EXPORTS.sql', 'DataTables_Website\webpages\exports.html')
    # create_plan_pages('DataTables_Website\SQL_queries\SCHEDULED_PLANS.sql')
    # create_plan_pages('DataTables_Website\SQL_queries\IMPORTS.sql')
    create_plan_pages('DataTables_Website\SQL_queries\SCHEDULED_PLANS.sql', 'DataTables_Website\SQL_queries\SCD_CONFIG.sql')