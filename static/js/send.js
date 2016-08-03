$(function() {
    $('button').click(function() {
        msg = document.getElementById('messagebox').value
        if (msg.charAt(0) == "!") {
            commands={ 
             "!rules":"<strong>RULES:</strong><br/>1) Respect others<br/>2) No impersonation<br/>3) No spam" 
            };
            if (commands[msg] == undefined) {
                $("<p id='rules'>Command not found</p>").hide().prependTo("#log").fadeIn("slow");
            } else {
                $("<p id='rules'>" + commands[msg] + "</p>").hide().prependTo("#log").fadeIn("slow");
            }
        } else {
            $.ajax({
                url: '/send',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            })
        };
    });
});
