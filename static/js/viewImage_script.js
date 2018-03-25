function initMap() {
	var marketLocation = {lat: {{ latitude }}, lng: {{ longitude }} };
		var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 4,
			center: marketLocation
		});
		var marker = new google.maps.Marker({
		position: marketLocation,
		map: map
	});
}