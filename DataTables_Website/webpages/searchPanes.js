function showSearchPanes() {
    current_page = window.location.href;

    if (current_page.includes('scheduled')) {
        search_index_arr = [0,1,2];
    } else if (current_page.includes('imports')) {
        // imports.html (panes to show: DataFormat Setup, Active Batch Path)
        search_index_arr = [4,5];
    } else if (current_page.includes('exports')) {
        // exports.html (panes to show: Active Batch Path, Extraction Setup, Entire Reference File String)
        search_index_arr = [3,5,8];
    } else if (current_page.includes('inventory')) {
        // inventory.html (panes to show: STATE, SCHEDULE_OR_TRIGGER)
        search_index_arr = [2,4];
    }

    $(document).ready(function() {
        var table = $('#table_id').DataTable({
            dom: 'Plfrtip',
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: search_index_arr
                }
            ],
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
            ],
        });
        table.searchPanes.container().prependTo(table.table().container());
        table.searchPanes.resizePanes();
        table.buttons().container().prependTo(table.table().container());
    });
}

showSearchPanes();
    
