function addClassToActivePage() {
    hrefArr = window.location.href.split('/');
    currentPage = hrefArr[hrefArr.length - 1].split('.')[0];
    switch (currentPage) {
        case 'scheduled': 
            var elem = document.getElementById("home-nav-a");
            break;
        case 'imports':
            var elem = document.getElementById("imports-nav-a");
            break;
        case 'exports':
            var elem = document.getElementById("exports-nav-a");
            break;
        case 'inventory':
            var elem = document.getElementById("inventory-nav-a");
            break;
        case 'timeline':
            var elem = document.getElementById("timeline-nav-a");
            break;
    }
    elem.classList.add('active');
}

addClassToActivePage();