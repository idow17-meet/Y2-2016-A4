$( document ).ready(function() {
    $('search').click( function() {
    	if (document.forms["Search"]['search'] === "" || document.forms["Search"]['search'] === null) {
    		alert("Field is empty");
    		return false;
    	}
    });
});