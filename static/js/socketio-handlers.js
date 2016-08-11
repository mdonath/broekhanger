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
		} else {
			speler = JSON.parse(speler);
			console.log('Naam: ' + speler.naam);
			$('#huidigespeler').text(speler.naam);
		}
	});

	socket.on('wachtrij', function(wachtrij) {
		console.log('Event: Wachtrij: ' + wachtrij);
		var lijst = JSON.parse(wachtrij);
		var w = $('#wachtrij');
		w.empty();
		$.each(lijst, function(i, speler) {
			w.append($('<li>')
				.append(
					$('<span>').addClass('speler').append(speler.naam)
					.click(function() {
						socket.emit('currentplayer', speler.id);
					})
				)
				.append($('<span>').addClass('email').append(speler.email))
				.append($('<span>').addClass('categorie').append(speler.categorie))
				.append($('<span>').addClass('removeplayer').append('[X]').click(function() {
	socket.emit('removeplayer', speler.id);
}))
			);
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

	/* Verwijdert de huidige speler */
	$('#huidige_speler').click(function(ev) {
		console.log("Sending: Player is done.");
		socket.emit('playerready');
	});
});
