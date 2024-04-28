let map;
let currentInfoWindow = null;

// Function to fetch restaurant data from the API
async function fetchRestaurants() {
    const response = await fetch('/api/restaurants');
    const restaurants = await response.json();
    return restaurants;
}

async function initMap() {
    const position = { lat: 60.1690699, lng: 24.9305591 };
  
    // Load the Google Maps API libraries
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const restaurants = await fetchRestaurants();
  
    // Initialize the map
    map = new Map(document.getElementById("map"), {
      zoom: 14,
      center: position,
      mapId: "70fdc3138886da7e",
      clickableIcons: false
    });
  
    restaurants.forEach(restaurant => {
        const { coord_x, coord_y, name, address } = restaurant;
        // Define the position object for the marker
        const position = { lat: coord_x, lng: coord_y };

        const iconImg = document.createElement("img");
        iconImg.src = "https://cdn-icons-png.flaticon.com/512/5193/5193679.png"
        iconImg.width = 48;
        iconImg.height = 48;

        // Create a marker for the restaurant
        const marker = new AdvancedMarkerElement({
            position: position,
            map: map,
            title: name,
            content: iconImg,
        });

        // Create an InfoWindow for the marker
        const infowindow = new google.maps.InfoWindow({
            content: "<big><a href='/restaurant/" + name.replace(/ /g, '_').replace(/'/g, '%27') + "'>" + name.replace(/'/g, "&#39;") + "</a></big><p>" + address + "</p>"
        });

        // Add a click event listener to the marker
        marker.addListener('click', function() {
            // Close the currently open InfoWindow (if any)
            if (currentInfoWindow) {
                currentInfoWindow.close();
            }
            // Open the InfoWindow for the current marker
            infowindow.open(map, marker);
            // Update the currentInfoWindow variable
            currentInfoWindow = infowindow;
        });

        // Add a click event listener to the map
        map.addListener("click", function(event) {
            // Close InfoWindows if any are open
            if (infowindow) {
                infowindow.close();
            }
        });
    });
}

initMap();
