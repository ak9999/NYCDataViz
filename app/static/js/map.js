// This example requires the Visualization library. Include the libraries=visualization
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization">



var map;
var heatmap;

function ready(fn){
    if(document.attachEvent ? document.readyState === "complete" : document.readyState != "loading"){
        fn();
    }else{
        document.addEventListener('DOMContentLoaded',fn);
    }
}


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {
            lat: 40.730815,
            lng: -73.997471
        },
        // Make it Night View
        styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#263c3f'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#6b9a76'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{color: '#38414e'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry.stroke',
              stylers: [{color: '#212a37'}]
            },
            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#746855'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#1f2835'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#17263c'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#515c6d'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#17263c'}]
            }
          ],
        mapTypeId: google.maps.MapTypeId.MAP,
        disableDefaultUI: true
    });
    var input = document.getElementById('pac-input');

    var autocomplete = new google.maps.places.Autocomplete(input);

    // Bing the map's bounds (view port ) property to the autocomplete object, 
    // so that the autocomplete request use the current map bounds for the 
    // bounds option in the requests.... Still don't really know what that means

    autocomplete.bindTo('bounds',map);

    autocomplete.addListener('place_changed', function(){
      var place = autocomplete.getPlace();
      map.fitBounds(place.geometry.viewpot);

    });
    
    var request = new XMLHttpRequest();
    request.open('GET', '/query', true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var data = JSON.parse(request.responseText);
            let result = [];
            for (var i = 0; i < data.length; i++) {
                result.push(new google.maps.LatLng(data[i].latitude, data[i].longitude));
            }
            console.log(result);
            heatmap = new google.maps.visualization.HeatmapLayer({
                data: result,
                map: map
            });
            changeGradient();
        }
    };
    request.onerror = function() {
        // There was a connection error of some sort

    };

    request.send();
}

ready(initMap);


function recv_data(data_url, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
            callback(xmlHttp.responseText);
        }
    };
    xmlHttp.open("GET", data_url, true); // asynchronous request
    xmlHttp.send(null);
}


function changeGradient() {
    var gradient = [
        'rgba(0, 255, 255, 0)',
        'rgba(0, 255, 255, 1)',
        'rgba(0, 191, 255, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(0, 63, 255, 1)',
        'rgba(0, 0, 255, 1)',
        'rgba(0, 0, 223, 1)',
        'rgba(0, 0, 191, 1)',
        'rgba(0, 0, 159, 1)',
        'rgba(0, 0, 127, 1)',
        'rgba(63, 0, 91, 1)',
        'rgba(127, 0, 63, 1)',
        'rgba(191, 0, 31, 1)',
        'rgba(255, 0, 0, 1)'
    ]
    heatmap.set('gradient', gradient);
}


