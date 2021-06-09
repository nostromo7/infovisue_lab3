const mapWidth = 800;
const mapHeight = 500;

selectedSeason = '2009/10';
selectedTeam = 'Arsenal';

let highlight = function(code) {
    d3.select('path#' + code.split(" ").join("_"))
        .attr('fill', 'CadetBlue')
        .attr('stroke-width', 2);
}

let undoHighlight = function(code) {
    d3.select('path#' + code.split(" ").join("_"))
        .attr('fill', 'white')
        .attr('stroke-width', 0.5);
}

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
            .attr('id', function(d) {return d.properties.admin.split(" ").join("_")})
            .attr('d', path)
            .attr('stroke', 'black')
            .attr('stroke-width', 0.5)
            .attr('fill', 'white');
    });
}

function initSeasons(seasons) {
    seasons = Object.values(JSON.parse(seasons));

    seasons_values = [...new Set(seasons.map(e => e.Season))];

    function updateSeason(season) {
        console.log(season);
        selectedSeason = season;
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
            updateSeason(d3.select(this).property('value'));
        });


}

function initTeams(standings) {
    standings = Object.values(JSON.parse(standings));
    teams = standings.map(e => e.Team)

    function updateTeam(team) {
        console.log(team);
        selectedTeam = team;
        d3.select('#players').selectAll('li')
        .data(players_sub).enter()
        .append('li')
        .text(function(d) {
            console.log(d);
            return d.short_name
        })
    }


    d3.select('#teams').selectAll('myOptions')
        .data(teams).enter()
        .append('option')
            .text(function(d) {return d})
            .attr('value', function(d) {
                return d
            });

    d3.select('#teams')
        .on('change', function(d) {
            updateTeam(d3.select(this).property('value'));
        });


}

function initPlayers(player) {
    players = Object.values(JSON.parse(player));
    console.log(players)

    players_sub = players.filter(p => p.club_name === selectedTeam)

    d3.select('#players').selectAll('li')
        .data(players_sub).enter()
        .append('li')
        .text(function(d) {
            return d.short_name + ' (' + d.nationality + ')';
        })
        .on('mouseover', function(d) {
            console.log(d)
            highlight(d.nationality);
        })
        .on('mouseout', function(d) {
            undoHighlight(d.nationality);
        });

}