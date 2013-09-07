// Going to need to resize rows in JavaScript to make this responsive.  Annoying.
(function(){

    var answers = [];
    var baseGameTemplate = "";

    // Helper funciton to start the timer
    function startTimer(duration, callback){
        $('#timer-region').animate({'width':'0%'}, duration, 'linear', callback);
    }

    // Basic exponential easing function, used to slowly change the bar to red
    $.easing.easeInExpo = function(t, millisecondsSince, startValue, endValue, totalDuration){
        //return Math.pow(Math.E, 10*t);
        return Math.pow(Math.E, 10*t)/(Math.pow(Math.E, 10));
    };

    $(document).ajaxError(function(evt, settings, err) {
        console.log(evt);
        console.log(settings);
        console.log(err);
    });

    /* Login */
    $(document).on('click touchstart', '#start-button', function(){
        // Ajax request
        $.get('/techs', {}, function(data, stat, xhr){
            $('.main-content').html(data);
        });
    });

    /* Tech selection */
    $(document).on('click touchstart', '.tech-block.selectable', function(){
        $(this).toggleClass('selected');
    });

    // On start, get the selected technologies, render the tour.  After the tour, render the game, and start the timer.
    $(document).on('click touchstart', '#start-block', function(){
        var selectedTechs = $('.tech-block.selected').map(function(i,e){return $(e).text()}).toArray();
        var questions = {};
        var index = 0; // The current question
        var answers = [];
        var gameCompleteHtml = "";
        $.get('/game', {"techs": selectedTechs.join(",")}, function(data, stat, xhr){
            questions = data;
            // Render base template, which requires asynchronous call to get the template from the server.
            // Then start the game
            renderBaseGameTemplate(function(){

                function playGame(){
                    // Render first question
                    renderQuestion(questions["questions"][0]);
                    // Start the timer
                    startTimer(90000,function(){
                        console.log("Done!");
                        var score = 0;
                        for (var i = 0; i<answers.length; i++){
                            if (answers[i]["playerAnswer"] === questions["questions"][i%questions["questions"].length]["answer"]){
                                score = score + 1;
                            }
                        }
                        /* Display finished modal; disable answers; collect answers, and request report*/
                        $('.main-content').html(gameCompleteHtml);
                    });
                }

                // Fetch empty template for "times up" screen
                $.get('/timesup', {}, function(data){
                    gameCompleteHtml = data;
                });

                // Show the tour
                $(document).foundation('joyride','start', {postRideCallback: playGame, modal: true, expose: true});
                // After the final modal, start the game
            });
        });

        $(document).on('click touchstart', '.answer-block', function() {
            // Store the answer
            $(this).css('color','green');
            console.log("The player answered " + $(this).html() + ", actual answer " + questions["questions"][index]["answer"]);
            var currQuestion = questions["questions"][index];
            answers.push({"question" : currQuestion["question"], "playerAnswer" : $(this).html()});
            index = index + 1;
            if (index === questions["questions"].length) {
                index = 0;
            }
            // Render the next question
            renderQuestion(questions["questions"][index]);
            // If index is getting close to the end, get more questions
            if (index >= questions["questions"].length - 3) {
                console.log("getting close to running out......");
            }
        });

        $(document).on('click touchstart', '.submit-results', function(){
            var playerInput = $('.player-email');
            if (playerInput[0].validity.valid){
                var player = playerInput.val();
                $.ajax('/result', {"type": "POST", "data": JSON.stringify({"player": player, "answers": answers}), "contentType":'application/json',
                    "success": function(data, stat, xhr){
                        $('.main-content').html(data);
                    }});
            } else {
                alert("Please provide a valid email address");
            }
        });
        return false;
    });

    // Helper functions
    function renderBaseGameTemplate(callback){
        // Compiled via doT; fix this.
        if (!baseGameTemplate){
            $.get('/baseGameTemplate',null,function(data){
                baseGameTemplate = data;
                $('.main-content').html(baseGameTemplate);
                callback();
            });
        } else {
            $('.main-content').html(baseGameTemplate);
            callback();
        }
    }

    function renderQuestion(question) {
        // Generate question section replacement.
        var questionText = getQuestionText(question);
        // Generate answer portion replacement.
        var answerHtml = renderAnswersToHtml(question);
        // Replace respective sections
        $('.question h3 pre').html(questionText);
        $('.answers').html(answerHtml);
    }

    function getQuestionText(question){
        return question.question;
    }

    // doTjs template function to render the question section.
    function renderAnswersToHtml(it /**/) { var out='';var arr1=it.options;if(arr1){var value,index=-1,l1=arr1.length-1;while(index<l1){value=arr1[index+=1];out+=' <div class="answer-block">'+( value )+'</div>';} } return out; }

}());
