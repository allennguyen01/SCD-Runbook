from unicodedata import name
from sql_to_dataframe import sql_to_dataframe
from dataframe_to_htmltable import dataframe_to_htmltable
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

            <script src="searchPanes.js"></script>
            <script src="https://www.gstatic.com/charts/loader.js"></script>
            <script src="timeline.js"></script>
        </head>
    <body>
        <div class="container-fluid">
            <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
                <a href="%(planPagePrefix)sscheduled.html" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                    <img class="me-4" src="%(planPagePrefix)simages\BCI-logo-250x129.png" alt="BCI" height="32px">
                    <h2 class="fw-bold mt-1">SCD Runbook</h2>
                </a>
        
                <ul class="nav nav-pills align-items-center">
                    <li class="nav-item">
                        <a href="%(planPagePrefix)sscheduled.html" class="nav-link" id="home-nav-a" onclick="addClassToActivePage()">
                            Scheduled Plans
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(planPagePrefix)simports.html" class="nav-link" id="imports-nav-a" onclick="addClassToActivePage()">
                            SCD Imports
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(planPagePrefix)sexports.html" class="nav-link" id="exports-nav-a" onclick="addClassToActivePage()">
                            SCD Exports
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(planPagePrefix)sinventory.html" class="nav-link" id="inventory-nav-a" onclick="addClassToActivePage()">
                            ActiveBatch Inventory
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(planPagePrefix)stimeline.html" class="nav-link" id="timeline-nav-a" onclick="addClassToActivePage()">
                            Timeline
                        </a>
                    </li>
                </ul>
            </header>
        </div>

        <div class="p-4 mb-4 bg-light rounded-3">
            <div class="container-fluid py-2">
                <h1 class="display-6 fw-bold">%(pageTitle)s</h1>
                <p class="col-md-12 fs-5">%(description)s</p>
                <div class="accordion" id="accordionExample">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                Table legend
                            </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                %(legend)s
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container-fluid">
            %(bodyContent)s
        </div>

        <script src="navbar.js"></script>
    </body>
</html>
    """

def create_table_template(sqlPath, outHTMLPath):
    df = sql_to_dataframe(sqlPath)

    # To be inserted into the page_template 
    tableHTML = dataframe_to_htmltable(df)

    # Extract the title of the page from the output file path name
    title = outHTMLPath.split('\\')[-1].split('.')[0]
    
    # Initialize variables for the page template
    bodyContent = tableHTML
    planPagePrefix = ''
    legend = ''
    if title == 'scheduled':
        pageTitle = 'Scheduled Plans'
        description = 'This page includes two datatables: ActiveBatch Scheduled Plans and Triggered Plans'
    elif title == 'imports':
        pageTitle = 'SCD Imports'
        description = 'Import files to SimCorp Dimension.'
    elif title == 'exports':
        pageTitle = 'SCD Exports'
        description = 'This page lists all the SCD Configuration objects that have a Batch Task of "Extracts Exporter Definitions - Execute", "Extraction Setups - Execute".'
        legend = '<strong>Batch Job Group | Batch Job:</strong> Identification field of Batch Job Group along with the Batch Job Name. <br> \
        <strong>Batch Job Name:</strong> Descriptive name of Batch Job.<br> \
        <strong>Reference File Export:</strong> Name of the reference file to write to.<br> \
        <strong>Entire Reference File String:</strong> Full Path of Reference File Export.<br> \
        <strong>LAN Output:</strong> If applicable, the output from the Batch Job to the LAN.<br> \
        <strong>Extraction Setup:</strong> If applicable, the ID of the Data extraction setup.<br> \
        <strong>Data Format Setup:</strong> If applicable (Destination Type = Message Queue), the ID of the Data Format Setup.<br> \
        <strong>Extract Table:</strong> If applicable (Destination Type = Extract table), the ID of the Data Format Setup.<br> \
        <strong>ActiveBatch Path:</strong> If applicable the Active Batch Plan that calls this Batch Job Group.'
    elif title == 'inventory':
        pageTitle = 'ActiveBatch Inventory'
        description = 'This page lists all the Active Batch plans that are: <br>\n \
        <ul class="fs-5">\n \
            <li><strong>Scheduled</strong>: have a schedule to start the job</li>\n \
            <li><strong>Triggered</strong>: arrival of a file</li>\n \
            <li><strong>Adhoc</strong>: no schedule or trigger, just ran adhoc</li>\n \
        </ul>\n'
        legend = '<strong>Name:</strong> Identification field of Batch Job Group.<br>\n \
            <strong>Path Name:</strong> Complete path of Active Batch Plan.<br>\n \
            <strong>Description:</strong> Description of the Active Batch Plan.<br>\n \
            <strong>State:</strong> If plan is enabled/disabled.<br>\n \
            <strong>Schedule or Trigger:</strong> Describes the schedule or Trigger for the Active Batch Plan.'

    # Create and write to a new HTML file
    with open(outHTMLPath, 'w') as f:
        f.write(page_template % vars())

def create_plan_pages(sqlPath, SCDConfigSQLPath):
    planDF = sql_to_dataframe(sqlPath)

    plan_template = """
        <h2>SCD Batch Job Group Execution</h2>
        %(bjgTableHTML)s
    """
    configDF = sql_to_dataframe(SCDConfigSQLPath)

    for i in range(len(planDF)):
        row = planDF.iloc[i]
        name = row['Name']

        planConfigDF = configDF.loc[configDF['Batch Job Group'] == name]
        bjgTableHTML = dataframe_to_htmltable(planConfigDF)

        # Initialize variables for the page template
        bodyContent = plan_template % vars()
        pageTitle = name
        description = 'If description or documentation available show here.'
        planPagePrefix = '..\\'
        
        with open(f"DataTables_Website\webpages\plan_pages\{name}.html", 'w') as f:
            f.write(page_template % vars())

if __name__ == '__main__':
    create_table_template('DataTables_Website\SQL_queries\SCHEDULED_PLANS.sql', 'DataTables_Website\webpages\scheduled.html')
    create_table_template('DataTables_Website\SQL_queries\IMPORTS.sql', 'DataTables_Website\webpages\imports.html')
    create_table_template('DataTables_Website\SQL_queries\EXPORTS.sql', 'DataTables_Website\webpages\exports.html')
    create_table_template('DataTables_Website\SQL_queries\ABAT_INVENTORY.sql', 'DataTables_Website\webpages\inventory.html')

    # create_plan_pages('DataTables_Website\SQL_queries\SCHEDULED_PLANS.sql', 'DataTables_Website\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('DataTables_Website\SQL_queries\ABAT_INVENTORY.sql', 'DataTables_Website\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('DataTables_Website\SQL_queries\IMPORTS.sql', 'DataTables_Website\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('DataTables_Website\SQL_queries\EXPORTS.sql', 'DataTables_Website\SQL_queries\SCD_CONFIG.sql')