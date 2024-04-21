let map;
let marker;
let infowindow;

async function initMap() {
  const position = { lat: 60.1690699, lng: 24.9305591 };

  // Load the Google Maps API libraries
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Initialize the map
  map = new Map(document.getElementById("map"), {
    zoom: 12,
    center: position,
    mapId: "70fdc3138886da7e",
  });

  // Create a marker and add it to the map
  marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "McDonalds",
  });

  // Initialize the InfoWindow
  infowindow = new google.maps.InfoWindow({
    content: "Add your popup content here",
  });

  // Add click event listener to the marker
  marker.addListener("click", function() {
    infowindow.open(map, marker);
  });

// Add a click event listener to the map
map.addListener("click", function(event) {
    // Close the InfoWindow if it is open
    if (infowindow) {
        infowindow.close();
    }
    });
}

initMap();