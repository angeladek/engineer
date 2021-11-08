function initLayers() {
    // Toevoegen OSM basemap
    let osmLayer = new ol.layer.Tile({
        source: new ol.source.OSM(),
        type: 'basemap',
        name: 'OpenStreetMap'
    });
    map.addLayer(osmLayer);

    //  Achtergrondlaag met ESRI satelliet 
    let ESRIsatteliet = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attributions: ['Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community']
        }),
        name: 'ESRI Satelliet',
        type: 'basemap'
    });
    map.addLayer(ESRIsatteliet);
    ESRIsatteliet.setVisible(false);

    // Toevoegen locatie has
    let hasSource = new ol.source.Vector();
    let hasLayer = new ol.layer.Vector({
        source: hasSource,
        type: 'vector',
        name: 'HAS vectorlaag'
    });
    map.addLayer(hasLayer);
    let hasFeature = new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat([5.2856336710073055, 51.686455625179036]))
    );
    hasSource.addFeature(hasFeature);

    //toevoegen WMS panden Den Bosch
    let pandendbSource = new ol.source.ImageWMS({
        url: 'https://gmd.has.nl/geoserver/proefstudeerdag/wms',
        params: {
            'layers': 'pandendb'
        }
    });
    let pandendbLayer = new ol.layer.Image({
        source: pandendbSource,
        type: 'wms',
        name: 'Panden Den Bosch'
    });
    map.addLayer(pandendbLayer); 
    // Toevoegen data GeoJSON

    // let postData = {
    //     'url': 'https://gmd.has.nl/geoserver/proefstudeerdag/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=proefstudeerdag:pandendb&outputFormat=application%2Fjson'
    // };

    // $.ajax({
    //     url: 'php/geoproxycurl.php',
    //     dataType: 'json',
    //     method: 'post',
    //     data: postData
    // }).done(function(data){
    //     hasSource.addFeatures(new ol.format.GeoJSON().readFeatures(data, {
    //         dataProjection: 'EPSG:4326',
    //         featureProjection: 'EPSG:3857'
    //     }));
    // }); 
    
    // let selectlLayerSource = new ol.source.Vector();
    // selectLayer = new ol.layer.Vector({
    //     source: selectlLayerSource,
    //     name: 'Select laag',
    //     type: 'select'
    // });
    // map.addLayer(selectLayer);

    // Voorbeeld styling wfs
    let postData = {
        'url': 'https://gmd.has.nl/geoserver/engineer2021/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=engineer2021:diversefeatures&maxFeatures=50&outputFormat=application%2Fjson'
    };

    $.ajax({
        url: 'php/geoproxycurl.php',
        dataType: 'json',
        method: 'post',
        data: postData
    }).done(function(data){
        voorbeeldStyleSource.addFeatures(new ol.format.GeoJSON().readFeatures(data, {
            dataProjection: 'EPSG:4326',
            featureProjection: 'EPSG:3857'
        }));
    }); 
    
    let voorbeeldStyleSource = new ol.source.Vector();
    voorbeeldStyleLayer = new ol.layer.Vector({
        source: voorbeeldStyleSource,
        name: 'Select laag',
        type: 'select',
        style: new ol.style.Style({
            image: blueMarker,
            fill: new ol.style.Fill({
                color: 'rgba(255, 0, 0, 0.2)'
            }),
            stroke: new ol.style.Stroke({
                color: 'purple',
                width: 3
            })
        })
    });
    map.addLayer(voorbeeldStyleLayer);

}

function buildLayerSwitcher() {
    map.getLayers().forEach(function(layer){
        console.log(layer)
        if (layer.get("type") == "basemap"){
            let ol_uid = layer.ol_uid;
            let liText = '<li><input type="radio" name="basemap" value="' + ol_uid + '" id="' + ol_uid + '" ';
            if (layer.getVisible()) {
                liText += 'checked';
            }
            liText += ' /><label for="' + ol_uid + '">' + layer.get("name") + '</label>'; 
            $('#baselayers').append(liText);
        } else if (layer.get("type") == 'wms' || layer.get("type") == 'vector') {
            let ol_uid = layer.ol_uid;
            let liText = '<li><input type="checkbox" name="overlaylayers" value="' + ol_uid + '" id="' + ol_uid + '" ';
            if (layer.getVisible()) {
                liText += 'checked';
            }
            liText += ' /><label for="' + ol_uid + '">' + layer.get("name") + '</label>'; 
            $('#overlaylayers').append(liText);
        }
    });

    $('input[type=radio][name=basemap]').on('change', function(){
        // console.log(this.value);
        let ol_uid = this.value;
        map.getLayers().forEach(function(layer){
            if(layer.ol_uid == ol_uid){
                layer.setVisible(true);
            } else if (layer.get("type") == 'basemap') {
                layer.setVisible(false);
            }   
        });
    });

    $('input[type=checkbox][name=overlaylayers]').on('change', function(){
        // console.log(this.value);
        let ol_uid = this.value;
        map.getLayers().forEach(function(layer){
            if(layer.ol_uid == ol_uid){
                if(layer.getVisible()){
                    layer.setVisible(false);
                } else {
                    layer.setVisible(true);
                }
            }
        });
    });

}