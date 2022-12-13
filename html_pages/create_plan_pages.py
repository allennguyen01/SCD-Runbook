from dataframe_to_htmltable import dataframe_to_htmltable
from sql_to_dataframe import sql_to_dataframe

page_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>%(page_title)s</title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link rel="stylesheet" href="%(plan_page_path)sstyles.css">

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

            <script src="%(plan_page_path)saddDataTablesFeatures.js"></script>
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
                <div class="h2 fw-bold">%(page_title)s</div>
                <p class="col-md-12 fs-5">%(description)s</p>
            </div>
        </div>

        <div class="container-fluid">
            %(body_content)s
        </div>

        <script src="%(plan_page_path)snavbar.js"></script>
    </body>
</html>
    """

def create_plan_pages(sql_path):
    plan_df = sql_to_dataframe(sql_path)

    plan_template = """
        <h4>SCD Batch Job Group Execution</h4>
        %(batchjobgroup_html_table)s
    """
    config_df = sql_to_dataframe('html_pages\SQL_queries\SCD_CONFIG.sql')

    for i in range(len(plan_df)):
        row = plan_df.iloc[i]
        name = row[0]
        if '|' in name:
            name = name.split(' | ')[0]

        plan_config_df = config_df.loc[config_df['Batch Job Group'] == name]
        if (plan_config_df.empty): 
            continue
        batchjobgroup_html_table = dataframe_to_htmltable(plan_config_df)

        # Initialize variables for the page template
        body_content = plan_template % vars()
        page_title = name
        description = 'If description or documentation available show here.'
        plan_page_path = '..\\'

        with open(f"html_pages\webpages\plan_pages\{name}.html", 'w') as f:
            f.write(page_template % vars())

if __name__ == '__main__':
    create_plan_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql')
    create_plan_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql')
    create_plan_pages('html_pages\SQL_queries\IMPORTS.sql')
    create_plan_pages('html_pages\SQL_queries\EXPORTS.sql')