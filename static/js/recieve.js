$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/msg');

	Array.prototype.remove = function() {
	    var what, a = arguments, L = a.length, ax;
	    while (L && this.length) {
	        what = a[--L];
	        while ((ax = this.indexOf(what)) !== -1) {
	            this.splice(ax, 1);
	        }
	    }
	    return this;
	};

    socket.on('newmsg', function(msg) {
        console.log("Received msg from " + msg.user + " that reads, " + msg.content)

        if (msg.user == "ALERT") {
	        msg_string = '<p id="alert"><strong>' + msg.user + ': </strong>' + msg.content + '</p>';
	    } else {
	        msg_string = '<p><strong>' + msg.user + ': </strong>' + msg.content + '</p>';
	    }

        $('#log').prepend($(msg_string).fadeIn('slow'));
    });

});
