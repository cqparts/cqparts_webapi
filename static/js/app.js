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

function PlugshowHide(){
	var p  = document.getElementById("plugins");
	var plus = document.getElementById("plus");
	if (plus.style.display === "none") {
		plus.style.display = "block";
		p.style.display = "none";
	} else {
		plus.style.display = "none";
		p.style.display = "block";
	}
}

