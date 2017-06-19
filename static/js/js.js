function main() {
    var pageNumber = 1;

    fetchData(pageNumber);

    $('#next').on('click', function() {
        pageNumber++;
        console.log(pageNumber);
        $('tbody').empty(); 
        fetchData(pageNumber);
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
            var planets = response.results
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
            }
        },
        error: function() {
            alert('Error loading planets data!');
        } 
    });
}

$(document).ready(main);