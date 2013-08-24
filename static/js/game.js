// Going to need to resize rows in JavaScript to make this responsive.  Annoying.
(function(){

    var answers = [];

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

    // On start, get the selected technologies, render the game, and start the timer.
    $(document).on('click touchstart', '#start-block', function(){
        var selectedTechs = $('.tech-block.selected').map(function(i,e){return $(e).text()}).toArray();
        var questions = {};
        var index = 0; // The current question
        var answers = []
        $.get('/game', {"techs": selectedTechs}, function(data, stat, xhr){
            questions = data;
            // Render base template
            renderBaseGameTemplate();
            // Render first question
            renderQuestion(questions["questions"][0]);
            // Start the timer
            startTimer(10000,function(){
                console.log("Done!");
                var score = 0;
                for (var i = 0; i<answers.length; i++){
                    if (answers[i]["userAnswer"] === questions["questions"][i%questions["questions"].length]["answer"]){
                        score = score + 1;
                    }
                }
                //$('.main-content').html('<h3><span style="color:red;">Times Up!</span></h3><h2>Score: ' + score + ' out of ' + answers.length + ' answers.</h2>');
                /* Display finished modal; disable answers; collect answers, and request report*/

                $('.main-content').html('<h3><span style="color:red;">Times up!</span></h3><form><fieldset><legend>Enter your email address to register and see your results</legend><div class="row"><div class="large-12 columns"><label>Email</label><input class="user-email" type="text" placeholder="example@me.com"><a href="#" class="button submit-results">Register</a></div></div></fieldset></form>');
            });

        });

        $(document).on('click touchstart', '.answer-block', function() {
            // Store the answer
            console.log("The user answered " + $(this).html() + ", actual answer " + questions["questions"][index]["answer"]);
            var currQuestion = questions["questions"][index];
            answers.push({"question" : currQuestion["question"], "userAnswer" : $(this).html()});
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
            var user = $('.user-email').val();
            $.ajax('/result', {"type": "POST", "data": JSON.stringify({"user": user, "answers": answers}), "contentType":'application/json',
                "success": function(data, stat, xhr){
                    $('.main-content').html(data); 
                }});
        });
    });

    /* Game */
    // Show "Ready", "Start", then start the game.


    // Helper functions
    function renderBaseGameTemplate(){
        // Compiled via doT; fix this.
        var out='<div class="game"> <div class="question-block"> <div class="timer"><div class="progress radius"><span id="timer-region" class="meter"></span></div></div> <hr> <div class="question"><h3><pre></pre></h3></div> <div class="notifications"></div> </div> <div class="answers"> </div></div>';
        $('.main-content').html(out);
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

    function renderAnswersToHtml(it /**/) { var out='';var arr1=it.options;if(arr1){var value,index=-1,l1=arr1.length-1;while(index<l1){value=arr1[index+=1];out+=' <div class="answer-block">'+( value )+'</div>';} } return out; }

}());
