function main() {
    
    // var test = '<img src="{{ url_for("static", filename="images/vote.png") }}" >';
    // $('h1').append(test);
    
    var userCookie = getUserCookie('username');
    console.log(userCookie);
    if (userCookie) {
        alert('logged in as ' + userCookie);
    } else {
        alert('logged out');
    };

    var pageNumber = 1;
    handlePlanets(pageNumber, userCookie);

    $('#next').on('click', function() {
        pageNumber++;
        console.log(pageNumber);
        $('#planets').empty(); 
        handlePlanets(pageNumber, userCookie);
    });

    $('#previous').on('click', function() {
        pageNumber--;
        console.log(pageNumber);
        $('#planets').empty();
        handlePlanets(pageNumber, userCookie); 
    });

    $('.test').on('click', function() {
        let data = JSON.stringify({planet:this.id});
        console.log('!!!!!!!!!!data ' + data); 
        $.ajax({
            type : 'POST',
            url : "/vote/",
            contentType: 'application/json;charset=UTF-8',
            data : JSON.stringify({data})
        })
        .done(function( msg ) {
            alert( "You have voted successfully! " + msg );
        })
        .fail(function( msg ) {
            alert( "Vote failed :-(" + msg );
        });
    });
}

function handlePlanets(page, cookie) {
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
            displayPlanets(response.results, cookie);
        },
        error: function() {
            alert('Error loading planets data!');
        } 
    });
}

function handlePageButtons(next, previous) {
    var $next = $('#next');
    var $previous = $('#previous');
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

function displayPlanets(planets, cookie) {
    var residentURLs = {};
    for (i = 0; i < planets.length; i++) {
        console.log(planets[i]);
        var planet = planets[i];
        var planetId = (planet.url).slice(28, -1);
        var name = planet.name;
        if (planet.diameter !== 'unknown') {
            var diameter = Number(planet.diameter).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' km';
        } else {
            var diameter = planet.diameter;
        };
        var climate = planet.climate;
        var terrain = planet.terrain;
        var surfaceWater = planet.surface_water;
        if (surfaceWater !== 'unknown') {
            surfaceWater = planet.surface_water + ' %';
        };
        if (planet.population !== 'unknown') {
            var population = Number(planet.population).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' people';
        } else {
            var population = planet.population;
        };
        var residentsArray = planet.residents;
        residentURLs[name] = residentsArray;
        console.log('residentURLs ' + residentURLs);
        switch(residentsArray.length) {
            case 0: {
                var residentsNumber = 'No known residents';
                break;    
            }
            case 1: {
                var residentsNumber = '<button id="' + name + '" type="button" data-toggle="modal" data-target="#residentsModal" class="btn btn-default resident">1 resident</button>';
                break;
            }
            default: {
                var residentsNumber = '<button id="' + name + '" type="button" data-toggle="modal" data-target="#residentsModal" class="btn btn-default resident">' + residentsArray.length + ' residents</button>'
                break;    
            }
        };
        if (cookie) {
            let imageTag = '<img src="/static/images/vote.png") class="vote" id="' + planetId + '" title="vote for ' + name + '" alt="vote" width="32" height="32">';
            console.log(imageTag);
            $('#planets').append('<tr><td>' + name + '</td><td>' + diameter + '</td><td>' + climate + '</td><td>' + terrain + '</td><td>' + surfaceWater + '</td><td>' + population + '</td><td>' + residentsNumber + '</td><td>' + imageTag + '</td></tr>');
        } else {
            $('#planets').append('<tr><td>' + name + '</td><td>' + diameter + '</td><td>' + climate + '</td><td>' + terrain + '</td><td>' + surfaceWater + '</td><td>' + population + '</td><td>' + residentsNumber + '</td></tr>');
        };
    };
    localStorage.setItem(residentURLs, residentURLs);
    console.log(localStorage);
    $('.resident').on('click', function() {
        console.log(this.id);
        console.log(name);
        $('.modal-title').append('Residents of ' + this.id);
        $('.close-modal').on('click', function() {
            $('#residentsModal').modal('hide');
            $('.modal-title').empty();
            $('#residents').empty();
        });
        var planetName = this.id;
        handleResidents(residentURLs[planetName]);
    });
    $('.vote').on('click', function() {
        alert(this.id);
        let vote = JSON.stringify({vote:this.id, username:cookie});
        console.log('!!!!!!!!!!vote ' + vote); 
        $.ajax({
            type : 'POST',
            url : "/vote/",
            contentType: 'application/json;charset=UTF-8',
            data : JSON.stringify({vote})
        })
        .done(function( msg ) {
            alert( "You have voted successfully! " + msg );
        })
        .fail(function( msg ) {
            alert( "Vote failed :-(" + msg );
        });
    });
}

function handleResidents(residents) {
    for (let i = 0; i < residents.length; i++) {
        console.log(residents[i]);
        handleResident(residents[i]);
    }
}

function handleResident(url) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: url,
        success: function(response) {
            displayResident(response);
        },
        error: function() {
            alert('Error loading planets data!');
        } 
    });
}

function displayResident(resident) {
    var name = resident.name;
    var height = (Number(resident.height)/100).toFixed(2) + ' m';
    if (resident.mass !== 'unknown') {
        var mass = resident.mass + ' kg';
    } else {
        var mass = resident.mass;
    };
    var skinColor = resident.skin_color;
    var hairColor = resident.hair_color;
    var eyeColor = resident.eye_color;
    var birthYear = resident.birth_year;
    var gender = resident.gender;
    $('#residents').append('<tr><td>' + name + '</td><td>' + height + '</td><td>' + mass + '</td><td>' + skinColor + '</td><td>' + hairColor + '</td><td>' + eyeColor + '</td><td>' + birthYear + '</td><td>' + gender + '</td></tr>');
}

function getUserCookie(cookieName) {
    let allcookies = document.cookie;
    var cookiearray = allcookies.split(';');
    var result = false
    for(let i = 0; i < cookiearray.length; i++) {
        name = cookiearray[i].split('=')[0];
        let value = cookiearray[i].split('=')[1];
        if (name === cookieName) {
            result = value;
            break;
        };
    };
    return result;  
};

$(document).ready(main);