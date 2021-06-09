const mapWidth = 800;
const mapHeight = 500;

function initMap() {

    // loads the world map as topojson
    d3.json("../static/data/world-topo.json").then(function (countries) {

        // defines the map projection method and scales the map within the SVG
        let projection = d3.geoEqualEarth()
            .scale(180)
            .translate([mapWidth / 2, mapHeight / 2]);

        // generates the path coordinates from topojson
        let path = d3.geoPath()
            .projection(projection);

        // configures the SVG element
        let svg = d3.select("#svg_map")
            .attr("width", mapWidth)
            .attr("height", mapHeight);

        // map geometry
        mapData = topojson.feature(countries, countries.objects.countries).features;

        // generates and styles the SVG path
        map = svg.append("g")
            .selectAll('path')
            .data(mapData)
            .enter().append('path')
            .attr('id', function(d) {return d.properties.admin})
            .attr('d', path)
            .attr('stroke', 'black')
            .attr('stroke-width', 0.5)
            .attr('fill', 'white');
    });
}

function initSeasons(seasons) {
    seasons = Object.values(JSON.parse(seasons));

    seasons_values = [...new Set(seasons.map(e => e.Season))];

    function updateSelection(season) {
        console.log(season)
    }

    d3.select('#seasons').selectAll('myOptions')
        .data(seasons_values).enter()
        .append('option')
            .text(function(d) {return d})
            .attr('value', function(d) {
                return d
            });

    d3.select('#seasons')
        .on('change', function(d) {
            updateSelection(d3.select(this).property('value'))
        });


}