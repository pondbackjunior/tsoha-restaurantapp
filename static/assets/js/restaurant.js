let map;
let marker;
let infowindow;

// Function to fetch restaurant data from the API
async function fetchRestaurants() {
    const response = await fetch('/api/restaurants');
    const restaurants = await response.json();
    return restaurants;
}

async function initMap(restaurantId) {
    const restaurants = await fetchRestaurants();
  
    const restaurant = restaurants.find(restaurant => restaurant.id === parseInt(restaurantId, 10));

    const defaultPosition = { lat: restaurant.coord_x, lng: restaurant.coord_y };
  
    // Load the Google Maps API libraries
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  
    // Initialize the map
    map = new Map(document.getElementById("map-restaurantpage"), {
        zoom: 16,
        center: defaultPosition,
        mapId: "70fdc3138886da7e",
        clickableIcons: false
    });

    if (restaurant) {
        const { coord_x, coord_y, name, address } = restaurant;
        // Define the position object for the marker
        const position = { lat: coord_x, lng: coord_y };

        const iconImg = document.createElement("img");
        iconImg.src = "https://cdn-icons-png.flaticon.com/512/5193/5193679.png";
        iconImg.width = 48;
        iconImg.height = 48;

        // Create a marker for the specific restaurant
        const marker = new AdvancedMarkerElement({
            position: position,
            map: map,
            title: name,
            content: iconImg,
        });

        // Create an InfoWindow for the marker
        const infowindow = new google.maps.InfoWindow({
            content: name
        });

        // Add a click event listener to the marker
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        // Add a click event listener to the map
        map.addListener("click", function() {
            // Close InfoWindows if any are open
            infowindow.close();
        });
    } else {
        console.log(`Restaurant with ID ${restaurantId} not found.`);
    }
}

const mapElement = document.getElementById("map-restaurantpage");
const restaurantId = mapElement.getAttribute("data-restaurant-id");
initMap(restaurantId);