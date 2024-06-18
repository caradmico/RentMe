<!-- Add Mapbox GL JS CSS -->
<link href="https://api.mapbox.com/mapbox-gl-js/v2.9.1/mapbox-gl.css" rel="stylesheet">
<!-- Add Mapbox GL JS -->
<script src="https://api.mapbox.com/mapbox-gl-js/v2.9.1/mapbox-gl.js"></script>
<script>
    mapboxgl.accessToken = 'pk.eyJ1IjoiY2FyYWRpYW5uZW1pY28iLCJhIjoiY2x3cjNhemowMDhtZTJsb2c1ZGp3dGZ6ZiJ9.slZ3YcKB_4OKBpr5dSTfSw'; // HouseMe token

    const map = new mapboxgl.Map({
        container: 'map', // container ID
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-122.4194, 37.7749], // starting position [lng, lat]
        zoom: 10 // starting zoom
    });

    // Load GeoJSON data and add as a layer
    map.on('load', function () {
        map.addSource('listings', {
            type: 'geojson',
            data: '/static/geojson/output.geojson' // Ensure this path is correct
        });

        map.addLayer({
            id: 'listings',
            type: 'circle',
            source: 'listings',
            paint: {
                'circle-radius': 5,
                'circle-color': '#007cbf'
            }
        });

        map.on('click', 'listings', function (e) {
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = `<strong>${e.features[0].properties.address}</strong><br>
                               Price: ${e.features[0].properties.price}<br>
                               Bedrooms: ${e.features[0].properties.bedroom}<br>
                               Square Footage: ${e.features[0].properties.squarefootage}<br>
                               Contact: ${e.features[0].properties.first_name} ${e.features[0].properties.last_name}<br>
                               Phone: ${e.features[0].properties.phone}<br>
                               Email: ${e.features[0].properties.email}`;

            // Ensure that if the map is zoomed out such that multiple copies of the feature are visible, the popup appears over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
        });

        // Change the cursor to a pointer when the mouse is over the listings layer.
        map.on('mouseenter', 'listings', function () {
            map.getCanvas().style.cursor = 'pointer';
        });

        // Change it back to a pointer when it leaves.
        map.on('mouseleave', 'listings', function () {
            map.getCanvas().style.cursor = '';
        });
    });
</script>
