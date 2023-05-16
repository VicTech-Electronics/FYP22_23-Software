var center_location = {lat: parseFloat(center_lat), lng: parseFloat(center_lng)};
var accident_location = {lat: parseFloat(accident_lat), lng: parseFloat(accident_lng)};

var MODE = document.getElementById('traveling_mode').value
var TYPE = document.getElementById('map_type_id').value

var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();



function initMap(){
    // Intitalize map
    var map = new google.maps.Map(document.getElementById('map'), {
        center: center_location,
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.TYPE,
    });
    
    // Adding markers
    var center_marker = new google.maps.Marker({
        position: center_location,
        map: map,
    });

    var accident_marker = new google.maps.Marker({
        position: accident_location,
        animation:google.maps.Animation.BOUNCE,
        map: map,
    });


    // Adding marker informations
    var center_info = new google.maps.InfoWindow({
        content: '<h6> Our location </h6>' + 
                center_country + '</br>' +
                center_city + '</br>' +
                center_region, 
    });

    var accident_info = new google.maps.InfoWindow({
        content: '<h6> Accident location </h6>' + 
                accident_country + '</br>' +
                accident_city + '</br>' +
                accident_region +  '</br>' +
                accident_ward,
    });

    // Adding event listerner to the markers
    center_marker.addListener('click', function(){
        center_info.open(map, center_marker);
    });

    accident_marker.addListener('click', function(){
        accident_info.open(map, accident_marker);
    });

    // Selet the map for direction display
    directionsDisplay.setMap(map);
}

function calcRoute(){
    var request = {
        origin: center_location,
        destination: accident_location,
        trevelMode: google.maps.TravelMode.MODE
    }

    directionsService.route(request, (result, status) => {
        if(status == google.maps.DirectionsStatus.OK){
            directionsDisplay.setDirections(result);
        }else{
            directionsDisplay.setDirections({route:[]})
            map.setCenter(center_location)
        }
    });
}


