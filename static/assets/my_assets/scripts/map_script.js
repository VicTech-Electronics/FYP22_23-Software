function initMap(){
    var location = {lat: latitude, lng: longitude};

    var options = {
        center: location,
        zoom: 16,
    };

    var map = new google.maps.Map(document.getElementById('map'), options);
    var marker = new google.maps.Marker({
        position: location,
        map: map,
    });

    var info = new google.maps.InfoWindow({
        content: "On " + date + ", Vehicle number " + vehicle_number + 'has got case at this place at ' + time,
    });

    marker.addListener('mouseover', function(){
        info.open(map, marker);
    });
}