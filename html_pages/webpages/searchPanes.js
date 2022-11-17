function showSearchPanes() {
    current_page = window.location.href;

    show_search_panes = true;

    if (current_page.includes('scheduled')) {
        panesToShow = [0,1,2];
        panesToHide = [];
    } else if (current_page.includes('imports')) {
        // imports.html (panes to show: DataFormat Setup, Active Batch Path)
        panesToShow = [4,5];
        panesToHide = [0,1,2,3];
    } else if (current_page.includes('exports')) {
        // exports.html (panes to show: Active Batch Path, Extraction Setup, Entire Reference File String)
        panesToShow = [3,5,8];
        panesToHide = [0,1,2,4,6,7];
    } else if (current_page.includes('inventory')) {
        // inventory.html (panes to show: state, schedule ot trigger)
        panesToShow = [2,4];
        panesToHide = [0,1,3];
    } else {
        panesToShow = [];
        panesToHide = [];
    }

    $(document).ready(function() {
        var table = $('#table_id').DataTable({
            dom: 'BPlfrtip',
            processing : true,
            searchPanes: {
                initCollapsed: true
            },
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: panesToShow
                },
                {
                    searchPanes: {
                        show: false
                    },
                    targets: panesToHide
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
        // table.searchPanes.container().prependTo(table.table().container());
        // table.searchPanes.resizePanes();
        // table.buttons().container().prependTo(table.table().container());
    });
}

showSearchPanes();
    
