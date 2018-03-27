function initMap() {
    var latitude = parseFloat($("#latitude").text());
    var longitude = parseFloat($("#longitude").text());

    var marketLocation = {lat: latitude, lng: longitude };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: marketLocation
    });
    var marker = new google.maps.Marker({
		position: marketLocation,
        map: map
    });
}