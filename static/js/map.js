const mapWidth = 800;
const mapHeight = 500;

let selectedSeason = '2016/17';
let selectedTeam = 'Arsenal';
let selectedCountries = [];
const MAX_SEASON = 2016;

//let tooltipPlayer = undefined;

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
        .attr('fill', function(d) {
            if (selectedCountries.includes(d.properties.admin)) {
                return 'gray';
            }
            else {
                return 'white';
            }
        })
        .attr('stroke-width', 0.5);
}

const highlightPlayers = function(countryCode) {
    highlightCountry(countryCode)
    d3.selectAll('.player').each(
        function(d) {
            if (d.nationality, d.nationality === countryCode) {
                d3.select(this).attr('style', 'text-decoration: underline;')
            }
        }
    )
}

const undoHighlightPlayers = function(countryCode) {
    undoHighlightCountry(countryCode)
    d3.selectAll('.player').each(
        function(d) {
            d3.select(this).attr('style', '')
        }
    )
}

const paintCountries = function() {
    d3.select("#svg_map").selectAll('path').each(
        function(d) {
            d3.select(this).attr('fill', function(d) {
                if (selectedCountries.includes(d.properties.admin)) {
                    return 'gray';
                }
                else {
                    return 'white';
                }
            })
        }
    );
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
            .attr('fill', function(d) {
                if (selectedCountries.includes(d.properties.admin)) {
                    return 'gray';
                }
                else {
                    return 'white';
                }
            })
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

    const seasons_values = [...new Set(seasons.map(e => e.Season))];
    let seasons_values_sub = seasons_values.filter(e => {
        return parseInt(e.split('/')[0]) <= MAX_SEASON;
    });
    seasons_values_sub = seasons_values_sub.reverse();

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
    let players_sub = players.filter(p => p.club_name === selectedTeam);
    players_sub = players_sub.sort(function(a, b) {
        return (a.overall > b.overall) ? -1 : 1;
    });
    selectedCountries = [...new Set(players_sub.map(e => e.nationality))];
    paintCountries();

    d3.select('#players').selectAll('*').remove();
    let tooltipPlayer = d3.select('body').append('div')
    .attr('class', 'tooltip')

    const showPlayerTooltip = function(player) {
        const textbox = tooltipPlayer
            .style('visibility', 'visible')
            .style('left', (d3.event.pageX + 20) + 'px')
            .style('top', (d3.event.pageY + 20) + 'px')

        textbox.append('text')
            .text('Nationality: ' + player.nationality);
        textbox.append('text')
            .text('Height: ' + player.height_cm/100 + 'm, Weight: ' + player.weight_kg + 'kg');
        textbox.append('text')
            .text(' - - - - - - - - - - - - - - - - - - - ');

        textbox.append('text')
            .text('Fifa21 Player-Stats:');
        textbox.append('text')
            .text('Overall Rating: ' + player.overall);
        if (!!player.shooting) {
             textbox.append('text')
                .text('Shooting: ' + player.shooting);
        }
        if (!!player.passing) {
            textbox.append('text')
                .text('Passing: ' + player.passing);
        }
        if (!!player.dribbling) {
            textbox.append('text')
                .text('Dribbling: ' + player.dribbling);
        }
        if (!!player.defending) {
            textbox.append('text')
                .text('Defense: ' + player.defending);
        }
        };

    const hidePlayerTooltip = function() {
        tooltipPlayer.selectAll('text').remove();
        tooltipPlayer.selectAll('hr').remove();
        tooltipPlayer.style('visibility', 'hidden')
    };

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
        .append('text')
            .html('<i class="fas fa-male"></i>')
        .append('text')
        .attr('class', 'player')
        .text(function(d) {
            return d.short_name + ' (Nr. ' + d.team_jersey_number + ')';
        })
        .on('mouseover', function(d) {
            d3.select(this).attr('style', "text-decoration: underline;");
            showPlayerTooltip(d);
            highlightCountry(d.nationality);
        })
        .on('mouseout', function(d) {
            d3.select(this).attr('style', "");
            hidePlayerTooltip();
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
    players = Object.values(JSON.parse(player));
    availableTeams = [...new Set(players.map(e => e.club_name))];

    const teams = standings.map(e => e.Team).filter(e => availableTeams.includes(e));

    d3.select('#teams').selectAll('myOptions')
        .data(teams).enter()
        .append('option')
            .text(function(d) {return d})
            .attr('value', function(d) {
                return d;
            });

    d3.select('#teams')
        .on('change', function(d) {
            updateTeam(d3.select(this).property('value'));
        });

   updateStandings(standings, selectedSeason);
}

function initPlayers() {
    updateTeam(selectedTeam)
}