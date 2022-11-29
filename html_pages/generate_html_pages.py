from sql_to_dataframe import sql_to_dataframe
from dataframe_to_htmltable import dataframe_to_htmltable

page_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>%(page_title)s</title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link rel="stylesheet" href="styles.css">

            <!-- Add jQuery and DataTables library and Bootstrap 5 integration -->
            <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.1.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.12.1/js/dataTables.bootstrap5.min.js"></script>
            <!-- <script src="..\html_pages\webpages\jquery-3.6.1.js"></script> -->
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
                <a href="index.html" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                    <img class="me-4" src="%(plan_page_path)simages\BCI-logo-250x129.png" alt="BCI" height="32px">
                    <h2 class="fw-bold mt-1">SCD Runbook</h2>
                </a>
        
                <ul class="nav nav-pills align-items-center">
                    <li class="nav-item">
                        <a href="%(plan_page_path)sscheduled.html" class="nav-link" id="home-nav-a" onclick="addClassToActivePage()">
                            Scheduled Plans
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(plan_page_path)simports.html" class="nav-link" id="imports-nav-a" onclick="addClassToActivePage()">
                            SCD Imports
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(plan_page_path)sexports.html" class="nav-link" id="exports-nav-a" onclick="addClassToActivePage()">
                            SCD Exports
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(plan_page_path)sinventory.html" class="nav-link" id="inventory-nav-a" onclick="addClassToActivePage()">
                            ActiveBatch Inventory
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="%(plan_page_path)stimeline.html" class="nav-link" id="timeline-nav-a" onclick="addClassToActivePage()">
                            Timeline
                        </a>
                    </li>
                </ul>
            </header>
        </div>

        <div class="p-4 mb-4 bg-light rounded-3">
            <div class="container-fluid py-2">
                <h1 class="display-6 fw-bold">%(page_title)s</h1>
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
            %(body_content)s
        </div>

        <script src="navbar.js"></script>
    </body>
</html>
    """

def create_table_pages(sql_path, out_html_path):
    df = sql_to_dataframe(sql_path)

    # To be inserted into the page_template 
    table_html = dataframe_to_htmltable(df)

    # Extract the title of the page from the output file path name
    title = out_html_path.split('\\')[-1].split('.')[0]
    
    # Initialize variables for the page template
    body_content = table_html
    plan_page_path = ''
    legend = ''
    if title == 'scheduled':
        page_title = 'Scheduled Plans'
        description = 'This page includes two datatables: ActiveBatch Scheduled Plans and Triggered Plans'
    elif title == 'imports':
        page_title = 'SCD Imports'
        description = 'Import files to SimCorp Dimension.'
    elif title == 'exports':
        page_title = 'SCD Exports'
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
        page_title = 'ActiveBatch Inventory'
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
    with open(out_html_path, 'w') as f:
        f.write(page_template % vars())

#BUGFIX: Get first column instead of column labeled 'Name'
def create_plan_pages(sql_path, scd_config_sql_path):
    plan_df = sql_to_dataframe(sql_path)

    plan_template = """
        <h2>SCD Batch Job Group Execution</h2>
        %(batchjobgroup_html_table)s
    """
    config_df = sql_to_dataframe(scd_config_sql_path)

    for i in range(len(plan_df)):
        row = plan_df.iloc[i]
        name = row['Name']

        plan_config_df = config_df.loc[config_df['Batch Job Group'] == name]
        batchjobgroup_html_table = dataframe_to_htmltable(plan_config_df)

        # Initialize variables for the page template
        body_content = plan_template % vars()
        page_title = name
        description = 'If description or documentation available show here.'
        plan_page_path = '..\\'
        legend = ''
        
        with open(f"html_pages\webpages\plan_pages\{name}.html", 'w') as f:
            f.write(page_template % vars())

if __name__ == '__main__':
    create_table_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql', 'html_pages\webpages\scheduled.html')
    # create_table_pages('html_pages\SQL_queries\IMPORTS.sql', 'html_pages\webpages\imports.html')
    # create_table_pages('html_pages\SQL_queries\EXPORTS.sql', 'html_pages\webpages\exports.html')
    # create_table_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql', 'html_pages\webpages\inventory.html')

    create_plan_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('html_pages\SQL_queries\IMPORTS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    # create_plan_pages('html_pages\SQL_queries\EXPORTS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')