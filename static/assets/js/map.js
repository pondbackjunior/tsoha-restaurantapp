window.onload = function() {
    L.mapquest.key = 'temp';

    var map = L.mapquest.map('map', {
        center: [49.7392, -104.903],
        layers: L.mapquest.tileLayer('map'),
        zoom: 6
    });

    L.marker([49.7392, -104.903], {
        icon: L.mapquest.icons.marker(),
        draggable: false
    }).bindPopup('Denver, CO').addTo(map);
};