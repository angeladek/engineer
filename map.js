function initMap() {
    map = new ol.Map({
        target: 'map',

        view: new ol.View({
            center: ol.proj.fromLonLat([5.293479538606579, 51.69977495687956]),
            zoom: 8
        })
    });
// oude popup
    let container = $('#popup').get(0);

    let popup = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });
    map.addOverlay(popup);

    $('#popup-closer').on('click', function(){
        popup.setPosition(undefined);
        $('#popup-closer').blur();
        return false;
    });

    //popup bootstrap
    // let featurepopup = new bootstrap.Modal(document)

    map.on('click', function(evt){
        popup.setPosition(undefined);
        // console.log(evt);
        // popup.setPosition(evt.coordinate);
        // let hdms = ol.coordinate.toStringHDMS(ol.proj.toLonLat(evt.coordinate));
        // $('#popup-content').html('<p>Je hebt hier geklikt: </p>' + hdms)

    //     map.forEachFeatureAtPixel(evt.pixel, function(feature){
    //         // console.log(feature.get("bouwjaar"));
    //         let bouwjaar;
    //         if(feature.get("bouwjaar")) {
    //             bouwjaar = feature.get("bouwjaar");
    //         } else {
    //             bouwjaar = "Is niet bekend";
    //         }
    //         let gebruiksdoel;
    //         if(feature.get("gebruiksdoel")) {
    //             gebruiksdoel = feature.get("gebruiksdoel");
    //         } else {
    //             gebruiksdoel = "Is niet bekend"
    //         }
            
    //         $('#popup-content').html('<p>bouwjaar: ' + bouwjaar + '</p><p>gebruiksdoel: ' + gebruiksdoel + '</p>');
    //         popup.setPosition(evt.coordinate);
    //     });
        map.forEachLayerAtPixel(evt.pixel, function(layer){
            console.log(layer);
            if (layer.get('type') == 'wms' && layer.get('name') == 'Panden Den Bosch'){
                let viewResolution = /** @type {number} */ (map.getView().getResolution());
                let getFeatureInfoUrl = layer.getSource().getFeatureInfoUrl(evt.coordinate, viewResolution, 'EPSG:3857', {
                    'INFO_FORMAT': 'application/json',
                    'QUERY_LAYERS': 'pandendb'
                });
                console.log(getFeatureInfoUrl);

                let postData = {
                    url: getFeatureInfoUrl
                }
                $.ajax({
                    url: 'PHP/geoproxycurl.php',
                    dataType: 'json',
                    method: 'post',
                    data: postData
                }).done(function(data){
                    console.log(data); 
                    if (data.features[0]) {
                        console.log(data.features[0].properties.bouwjaar);
                        // Vectorlaag selecteren
                        selectLayer.getSource().clear();
                        selectLayer.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(data.features[0]));
                        let feature = selectLayer.getSource().getFeatures()[0];
 
                        let zoom = map.getView().getZoom();
                        if (map.getView().getZoom() < 15) {
                            zoom = 15;
                        }
 
                        console.log(ol.extent.getCenter(feature.getGeometry().getExtent()));
                        map.getView().animate({
                            center: ol.extent.getCenter(feature.getGeometry().getExtent()),
                            zoom: zoom
                        });
                    let bouwjaar = data.features[0].properties.bouwjaar;
                    let gebruiksdoel = data.features[0].properties.gebruiksdoel;
                    $('#popup-content').html('<p>bouwjaar: ' + bouwjaar + '</p><p>gebruiksdoel: ' + gebruiksdoel + '</p>');
                    // $('#popup-content').html(data);
                    popup.setPosition(evt.coordinate);
                    } else {
                        $('#popup-content').html("<h2>Er is geen data gevonden</h2>")
                        popup.setPosition(evt.coordinate);
                    }
                    
                });
            }
        });

    });

    



}