// Initialize and add the map
function initMap() {
    // The location of the main restaurant plus the coordinates/id/names of related restaurants to populate the map

    var longitude = Number($("#lng").val());
    var latitude = Number($("#lat").val());
    var rel_rests = $(".rel_rests")
    
    
    
    const restaurant_loc = { lat: latitude, lng: longitude };
    // The map, centered on the main restaurant
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: restaurant_loc,
        options: {
            gestureHandling: 'greedy'
        }
    });
// related restaurants markers
    var markers = [];
    for(var i = 0; i < rel_rests.length; i++){ 
        var coords = ($(rel_rests[i]).val().split("/"));
        const latLng = new google.maps.LatLng(coords[0], coords[1]);
        const restRec = new google.maps.Marker({
            title: coords[2],
            position: latLng,
            map: map,
            url: "/dashboard/restaurants/show/"+coords[3],
        });
        markers.push(latLng);
    
        google.maps.event.addListener(restRec, 'click', function() {
            window.location.href = restRec.url;
        });
    }
    // creating bounds to zoom to correct level containing all related restaurant markers
    if (markers.length > 0) {
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < markers.length; i++) {
        bounds.extend(markers[i]);
        }
        map.fitBounds(bounds);
    }
    // var MarkerCluster = new MarkerClusterer(map, markers);
    

    // The marker for the main restaurant
    var icon = {
        url: "/media/images/pin.png",
        scaledSize: new google.maps.Size(40, 40), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(0, 0) // anchor
    };

    const marker = new google.maps.Marker({
        position: restaurant_loc,
        icon: icon,
        map: map,
        label: "You are Here"
    });
}



