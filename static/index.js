new Vue({
    el: '#main',
    data: {
        place_list: []
    },
    mounted() {
        axios.get('/api/map/bydomain/')
            .then(response => {
                let map_bounds = response.data['bounds']
                this.map = L.map('map').fitBounds(map_bounds);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(this.map);
                axios.get(response.data['url_place_list'])
                    .then(response => {
                        response.data.forEach(place => {
                            place.marker = L.marker([place.latitude, place.longitude]).addTo(this.map).bindPopup(place.name).openPopup();
                            this.place_list.push(place);
                        });
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
