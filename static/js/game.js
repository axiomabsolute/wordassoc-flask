// Going to need to resize rows in JavaScript to make this responsive.  Annoying.
(function(){

    // Helper funciton to start the timer
    function startTimer(duration, callback){
        $('#timer-region').animate({'width':'0%'}, duration, 'linear', callback);
    }

    // Callback function when the game is done
    function completeGame(){

    }

    // Basic exponential easing function, used to slowly change the bar to red
    $.easing.easeInExpo = function(t, millisecondsSince, startValue, endValue, totalDuration){
        //return Math.pow(Math.E, 10*t);
        return Math.pow(Math.E, 10*t)/(Math.pow(Math.E, 10));
    };

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

    $(document).on('keydown', '#login-email-input', function(event){
        if (event.keyCode == 13 && $(this).val()){
            $('#login-button').click();
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
            startTimer(25000,function(){console.log("Done!");});
        });
    });

    /* Game */
    // Show "Ready", "Start", then start the game.
}());
