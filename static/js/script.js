// purseFloat()
function initMap(){
    location = {lat: -6.776012, lng: 39.178326};

    options = {
        center: location,
        zoom: 16
    };

    var map = new google.maps.Map(document.getElementById('map'), options);

    var marker = new google.Marker({
        position: location,
        map: map,
    });

    var infomation = new google.maps.InfoWindow({
        content: 'Child location'
    });

    marker.addListener('mouseover', function(){
        infomation.open(map, marker);
    });
}