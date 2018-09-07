// show hide

function showHide(){
	var x = document.getElementById("info");
	var show = document.getElementById("show");
	if (x.style.display === "none") {
		x.style.display = "block";
		show.style.display = "none";
	} else {
		x.style.display = "none";
		show.style.display = "block";
	}
}

