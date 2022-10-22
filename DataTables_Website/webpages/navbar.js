function addClassToActivePage() {
    current_page = window.location.href

    if (current_page.includes('index')) {
        var elem = document.getElementById("home-nav-a")
        elem.classList.add('active')
    } else if (current_page.includes('imports')) {
        var elem = document.getElementById("imports-nav-a")
        elem.classList.add('active')
    } else if (current_page.includes('exports')) {
        var elem = document.getElementById("exports-nav-a")
        elem.classList.add('active')
    }

    // switch (page) {
    //     case 'home': 
    //         var elem = document.getElementById("home-nav-a")
    //         elem.classList.add('active')
    //     case 'imports':
    //         var elem = document.getElementById("imports-nav-a")
    //         elem.classList.add('active')
    //     case 'exports':
    //         var elem = document.getElementById("exports-nav-a")
    //         elem.classList.add('active')
    // }
}