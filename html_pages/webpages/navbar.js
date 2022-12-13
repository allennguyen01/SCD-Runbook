function activateNavbar() {
	hrefArray = window.location.href.split("/");
	currentPage = hrefArray[hrefArray.length - 1].split(".")[0];
	let elem = document.getElementById(`${currentPage}-nav`);
	elem.classList.add("active");
}

activateNavbar();
