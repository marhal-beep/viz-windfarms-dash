window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, context) {
            mmarker = L.circleMarker(latlng, {
                radius: 5,
                fillOpacity: 0.5
            }).bindPopup("Displayed");
            return mmarker.openPopup();
        }
    }
});