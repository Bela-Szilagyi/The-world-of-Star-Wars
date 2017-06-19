function main() {
    var pageNumber = 1;

    fetchData(pageNumber);

    $('#next').on('click', function() {
        pageNumber++;
        console.log(pageNumber);
        $('tbody').empty(); 
        var result = fetchData(pageNumber);
    });

    $('#previous').on('click', function() {
        pageNumber--;
        console.log(pageNumber);
        $('tbody').empty(); 
        var result = fetchData(pageNumber);
    });
}

function fetchData(page) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://swapi.co/api/planets/?page=' + page,
        success: function(response) {
            console.log(response.count);
            console.log(response.next);
            console.log(response.previous);
            console.log(response.results);
            console.log(response.results.length);
            handlePageButtons(response.next, response.previous);
            displayResults(response.results);
        },
        error: function() {
            alert('Error loading planets data!');
        } 
    });
}

function handlePageButtons(next, previous) {
    var $next = $('#next');
    var $previous = $('#previous');
    if ($previous.hasClass('disabled')) {
        console.log('previous disabled');
    } else {
        console.log('previous enabled');
    };
        if ($next.hasClass('disabled')) {
        console.log('next disabled');
    } else {
        console.log('next enabled');
    };
    if (next !== null) {
        console.log('next ok');
    } else {
        console.log('next not ok');
    };
        if (previous !== null) {
        console.log('previous ok');
    } else {
        console.log('previous not ok');
    };
    if ($next.hasClass('disabled') && next !== null) {
        console.log('enabling next');
        $next.removeClass('disabled');
        $next.removeProp('disabled');
    };
    if (! $next.hasClass('disabled') && next === null) {
        console.log('disabling next');
        $next.addClass('disabled');
        $next.prop('disabled', 'disabled');
    };
    if ($previous.hasClass('disabled') && previous !== null) {
        console.log('enabling previous');
        $previous.removeClass('disabled');
        $previous.removeProp('disabled');
    };
    if (! $previous.hasClass('disabled') && previous === null) {
        console.log('disabling previous');
        $previous.addClass('disabled');
        $previous.prop('disabled', 'disabled');
    };
}

function displayResults(planets) {
    for (i = 0; i < planets.length; i++) {
    console.log(planets[i]);
    let planet = planets[i];
    let name = planet.name;
    let diameter = Number(planet.diameter).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' km';
    let climate = planet.climate;
    let terrain = planet.terrain;
    let surfaceWater = planet.surface_water;
    if (surfaceWater !== 'unknown') {
        surfaceWater = planet.surface_water + ' %';
    };
    if (planet.population !== 'unknown') {
        var population = Number(planet.population).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' people';
    } else {
        var population = planet.population;
    };
    let residents = planet.residents;
    switch(residents.length) {
        case 0: {
            residents = 'No known residents';
            break;    
        }
        case 1: {
            residents = '<button type="button" class="btn btn-default">1 resident</button>';
            break;
        }
        default: {
            residents = '<button type="button" class="btn btn-default">' + residents.length + ' residents</button>'
            break;    
        }
    };
    $('tbody').append('<tr><td>' + name + '</td><td>' + diameter + '</td><td>' + climate + '</td><td>' + terrain + '</td><td>' + surfaceWater + '</td><td>' + population + '</td><td>' + residents + '</td></tr>');
    };
}

$(document).ready(main);