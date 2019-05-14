new Vue({
    el: '#main',
    data: {
        place_list: []
    },
    mounted() {
        this.map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(this.map);
        axios.get('/api/map/bydomain/')
            .then(response => {
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
