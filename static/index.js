new Vue({
    el: '#main',
    data: {
        map_name: "",
        place_list: []
    },
    mounted() {
        axios.get('/api/maps/bydomain/?expand=places')
            .then(response => {
                let map_bounds = response.data['bounds'];
                this.map_name = response.data['name'];
                this.map = L.map('map').fitBounds(map_bounds);
                L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {}).addTo(this.map);
                response.data['places'].forEach(place => {
                    var color = 'blue';
                    if (place.note_mean < 4) {
                        color = 'red';
                    } else if (place.note_mean < 7) {
                        color = 'orange';
                    } else if (place.note_mean >= 7) {
                        color = 'green';
                    }
                    var icon = new L.Icon({
                        iconUrl: `https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    });
                    place.marker = L.marker([place.latitude, place.longitude], {icon: icon}).addTo(this.map).bindPopup(place.name).openPopup();
                    this.place_list.push(place);
                });
            });
    },
    methods: {
        centerMapOn(place) {
            this.map.flyTo([place.latitude, place.longitude]);
            place.marker.openPopup();
        },
    }
});
