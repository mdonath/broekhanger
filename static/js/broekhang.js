$(document).ready(function() {
	// Connect to socketio server.
       var socket = io.connect();

	socket.on('connect', function() {
		console.log('Event: Connected!');
		$('#status').text('Connected!');
	});

	socket.on('disconnect', function() {
		console.log('Event: Disconnected!');
		$('#status').text('Disconnected!');
	});

	socket.on('status', function(new_status) {
		console.log('Event: Status: ' + new_status);
		$('#status').text(new_status);
	});

	socket.on('foto', function(url) {
		console.log('Event: Nieuwe foto: ' + url);
		$('#laatste_foto').attr('src', url + '?rnd='+Math.random());
	});

	socket.on('tijd', function(tijd) {
		console.log('Event: Tijd: ' + tijd);
		$('#klok').text(tijd);
	});

	socket.on('sensor_broek', function(waarde) {
		console.log('Event: Broek: ' + waarde);
		$('#broek').text(waarde);
	});

	socket.on('sensor_plank', function(waarde) {
		console.log('Event: Plank: ' + waarde);
		$('#plank').text(waarde);
	});

	socket.on('huidige_speler', function(speler) {
		console.log('Event: Nieuwe speler: ' + speler);
		if (speler == 'null') {
			$('#huidigespeler').text('Niemand!');
			$('#spelerisklaar,#spelerterug').hide();
		} else {
			speler = JSON.parse(speler);
			console.log('Naam: ' + speler.naam);
			$('#huidigespeler').text(speler.naam);
			$('#spelerisklaar,#spelerterug').show();
		}
	});

	socket.on('scores', function(spelers) {
		console.log('Events: Scores: ' + spelers);
		var lijst = JSON.parse(spelers);
		var categorien = ['G', 'M', 'K'];
		$.each(categorien, function (i, categorie) {
			var categorie_lijst = [];
			$.each(lijst, function(i, speler) {
				if (speler.categorie == categorie && speler.scores && speler.scores.length > 0) {
					categorie_lijst.push(speler);
				}
			});
			if (categorie_lijst.length > 0) {
				// sorteer de lijst
				categorie_lijst.sort(function(a,b) {
					if (a.scores[0] < b.scores[0]) {
						return 1;
					}
					if (a.scores[0] > b.scores[0]) {
						return -1;
					}
					return 0;
				});
				var w = $('#scores_' + categorie + ' tbody');
				w.empty();
				var aantal_spelers = 0;
				$.each(categorie_lijst, function(i, speler) {
					aantal_spelers++;
					w.append($('<tr>')
						.append($('<td>').addClass('spelerid').append(aantal_spelers) )
						.append($('<td>').addClass('speler').append(speler.naam) )
						.append($('<td>').addClass('email').append(speler.email) )
						.append($('<td>').addClass('score').append(speler.scores[0]) )
					)
					// Toon top 3
					if (aantal_spelers == 3) {
						return false;
					}
				});
			}
		})
	});

	socket.on('wachtrij', function(wachtrij) {
		console.log('Event: Wachtrij: ' + wachtrij);
		var lijst = JSON.parse(wachtrij);
		var w = $('#wachtrij tbody');
		w.empty();
		$.each(lijst, function(i, speler) {
			w.append($('<tr>')
				.click(function() { socket.emit('currentplayer', speler.id); })
				.attr('role', 'button')
				.append($('<td>').addClass('spelerid').append(speler.id) )
				.append($('<td>').addClass('speler').append(speler.naam) )
				.append($('<td>').addClass('email').append(speler.email) )
				.append($('<td>').addClass('categorie').append($('<span>').addClass('badge').append(speler.categorie) ))
				.append($('<td>')
					.append($('<span>')
						.attr('role', 'button')
						.addClass('removeplayer glyphicon glyphicon-trash')
						.click(function() { socket.emit('removeplayer', speler.id); })
					)
				)
			)
		});
	});

	/* Resets the game. */
	$('#reset').click(function(ev) {
		console.log("Sending reset");
		socket.emit('reset');
	});

	/* Adds new player. */
	$('#addplayer').click(function(ev) {
		var naam = $('#naam').val();
		var email = $('#email').val();
		var categorie = $('input[name=categorie]:checked').val()
		console.log("Sending addplayer "+ categorie);
		socket.emit('addplayer', naam, email, categorie);
	});
	
	/* Neemt een test foto */
	$('#takepicture').click(function(ev) {
		console.log("Sending: Take a Picture");
		socket.emit('takepicture');
	});

	/* Zet het systeem uit */
	$('#poweroff').click(function(ev) {
		console.log("Sending: poweroff");
		socket.emit('poweroff');
	});

	/* Verwijdert de huidige speler */
	$('#spelerisklaar').click(function(ev) {
		console.log("Sending: Player is done.");
		socket.emit('playerready');
	});

	/* Een speler gaat weer terug achteraan de wachtrij. */
	$('#spelerterug').click(function(ev) {
		console.log("Sending: Player back in queue.");
		socket.emit('currentplayerbackqueue');
	});
});
