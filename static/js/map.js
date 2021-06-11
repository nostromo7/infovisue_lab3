const mapWidth = 800;
const mapHeight = 500;

selectedSeason = '2009/10';
selectedTeam = 'Arsenal';

maxSeason = 2016;

let countryNameHelper = function(name) {
    return name.split(" ").join("_");
}

let highlightCountry = function(code) {
    d3.select('path#' + countryNameHelper(code))
        .attr('fill', 'CadetBlue')
        .attr('stroke-width', 2);
}

let undoHighlightCountry = function(code) {
    d3.select('path#' + countryNameHelper(code))
        .attr('fill', 'white')
        .attr('stroke-width', 0.5);
}

let highlightPlayers = function(countryCode) {
    highlightCountry(countryCode)
    d3.selectAll('.player').each(
        function(d) {
            if (d.nationality, d.nationality === countryCode) {
                d3.select(this).attr('style', 'text-decoration: underline;')
            }
        }
    )
}

let undoHighlightPlayers = function(countryCode) {
    undoHighlightCountry(countryCode)
    d3.selectAll('.player').each(
        function(d) {
            d3.select(this).attr('style', '')
        }
    )
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
            .attr('id', function(d) {return countryNameHelper(d.properties.admin)})
            .attr('d', path)
            .attr('stroke', 'black')
            .attr('stroke-width', 0.5)
            .attr('fill', 'white')
            .on('mouseover', function(d) {
                highlightPlayers(d.properties.admin);
            })
            .on('mouseout', function(d) {
                undoHighlightPlayers(d.properties.admin);
            });
    });
}

function initSeasons(seasons, standings) {
    seasons = Object.values(JSON.parse(seasons));
    standings = Object.values(JSON.parse(standings));

    seasons_values = [...new Set(seasons.map(e => e.Season))];
    seasons_values_sub = seasons_values.filter(e => {
        return parseInt(e.split('/')[0]) <= maxSeason;
    });

    d3.select('#seasons').selectAll('myOptions')
        .data(seasons_values_sub).enter()
        .append('option')
            .text(function(d) {return d})
            .attr('value', function(d) {
                return d
            });

    d3.select('#seasons')
        .on('change', function(d) {
            updateStandings(standings, d3.select(this).property('value'));
        });


}

function updateTeam(team) {
    selectedTeam = team;
    players_sub = players.filter(p => p.club_name === selectedTeam)
    d3.select('#players').selectAll('*').remove();

    if (players_sub.length === 0) {
     d3.select('#players')
        .append('li')
        .append('text')
        .text('No Fifa21-stats for this Team');
    }
    else {
        d3.select('#players').selectAll('li')
        .data(players_sub).enter()
        .append('li')
        .attr('id', function(d) {
            return countryNameHelper(d.sofifa_id.toString())})
        .append('g')
        .attr("font-family", "'Font Awesome 5 Free'")
        .attr("font-weight", 900)
        .text("\uf007")
        .append('text')
        .attr('class', 'player')
        .text(function(d) {
            return d.short_name + ' (' + d.nationality + ')';
        })
        .on('mouseover', function(d) {
            d3.select(this).attr('style', "text-decoration: underline;")
            highlightCountry(d.nationality);
        })
        .on('mouseout', function(d) {
            d3.select(this).attr('style', "")
            undoHighlightCountry(d.nationality);
        });
    }

}

function updateStandings(standings, seasonSelection) {
    selectedSeason = seasonSelection;
    selectedSeason_sub = selectedSeason.split('/')[0];
    standings_sub = standings.filter(e => e[selectedSeason_sub] !== null)
    standings_sub = standings_sub.sort(function(a, b) {
        return a[selectedSeason_sub] - b[selectedSeason_sub];
    })
    d3.select('#standings').selectAll('li').remove();

    d3.select('#standings').selectAll('li')
        .data(standings_sub).enter()
        .append('li')
        .text(function(d,i) {
            return (i+1) + '. ' + d.Team;
        })
}

function initTeams(standings, player) {
    standings = Object.values(JSON.parse(standings));
    teams = standings.map(e => e.Team)
    players = Object.values(JSON.parse(player));

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

   updateStandings(standings, selectedSeason);
}

function initPlayers(player) {
    players = Object.values(JSON.parse(player));

    updateTeam(selectedTeam)
    players_sub = players.filter(p => p.club_name === selectedTeam)
}