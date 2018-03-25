function initMap() {
    var marketLocation = {lat: {{ existing_image.latitude }}, lng: {{ existing_image.longitude }} };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: marketLocation
    });
    var marker = new google.maps.Marker({
		position: marketLocation,
        map: map
    });
}