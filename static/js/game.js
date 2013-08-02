// Going to need to resize rows in JavaScript to make this responsive.  Annoying.
(function(){
    /* Login */
    $(document).on('click', '#login-button', function(){
        var email = $('#login-email-input').val();
        if (!email){
            console.log("Alert the user to provide an email.  Also check if valid");
        } else {
            // Ajax request
            $.get('/techs', {"email": email}, function(data, stat, xhr){
                $('.main-content').html(data);
            });
        }
    });

    /* Tech selection */
    $(document).on('click', '.tech-block', function(){
        $(this).toggleClass('selected');
    });

    // On start, get the selected technologies, render the game, and start the timer.
    $(document).on('click', '#start-block', function(){
        var selectedTechs = $('.tech-block.selected').map(function(i,e){return $(e).text()}).toArray();
        $.get('/game', {"techs": selectedTechs}, function(data, stat, xhr){
            console.log(data);
            $('.main-content').html(data);
            // Start the timer
        });
    });

    /* Game */
}());
