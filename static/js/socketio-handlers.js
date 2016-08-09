$(document).ready(function() {
	// Connect to socketio server.
       var socket = io.connect();

	socket.on('connect', function() {
		console.log('Connected!');
		$('#status').text('Connected!');
	});

	socket.on('disconnect', function() {
		console.log('Disconnected!');
		$('#status').text('Disconnected!');
	});

	socket.on('status', function(new_status) {
		console.log('Status: ' + new_status);
		$('#status').text(new_status);
	});

	socket.on('foto', function(url) {
		console.log('Nieuwe foto: ' + url);
		$('#foto').attr('src', '');
		$('#foto').attr('src', url);
	});

	socket.on('tijd', function(tijd) {
		console.log('Tijd: ' + tijd);
		$('#klok').text(tijd);
	});

	socket.on('sensor_broek', function(waarde) {
		console.log('Broek: ' + waarde);
		$('#broek').text(waarde);
	});

	socket.on('sensor_plank', function(waarde) {
		console.log('Plank: ' + waarde);
		$('#plank').text(waarde);
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
});
