new Vue({
    el: '#main',
    data: {
        place_list: []
    },
    mounted() {
        var map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);
        axios.get('/api/map/bydomain/')
            .then(response => {
                axios.get(response.data['url_place_list'])
                    .then(response => {
                        response.data.forEach(place => {
                            this.place_list.push(place);
                            L.marker([place.latitude, place.longitude]).addTo(map).bindPopup(place.name).openPopup();
                        });
                    });
            });
    }
});
