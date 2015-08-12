var number;
function addFields() {
	number = document.getElementById("numppl").value;
	var people = document.getElementById("people");

	while (people.hasChildNodes()) {
		people.removeChild(people.lastChild);
	}

	for (i=0; i<number; i++) {

		html = $("<div class='row'>").append($("<div class='input-field col s3 dyn'>")
    	.append(document.createTextNode("Person " + (i+1))).append("<input type=text class='dynamic'" + " name=p" + String(i) + ">"));

    	$("#people").append(html);
	}

	var finished = $("#final");
	finished.prop("disabled", false);
	finished.removeClass("disabled");
}
