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

    // On start, get the selected technologies, render the tour.  After the tour, render the game, and start the timer.
    $(document).on('click touchstart', '#start-block', function(){
        var selectedTechs = $('.tech-block.selected').map(function(i,e){return $(e).text()}).toArray();
        var sampleQuestion = {"question" : "if(i < 5){...}", "options" : ["Iteration","Conditional", "Assignment", "Composition"]};
        var questions = {};
        var index = 0; // The current question
        var answers = []
        $.get('/game', {"techs": selectedTechs}, function(data, stat, xhr){
            questions = data;
            // Render base template
            renderBaseGameTemplate();
            // Render example question
            renderQuestion(sampleQuestion);

            function playGame(){
                // Render first question
                renderQuestion(questions["questions"][0]);
                // Start the timer
                startTimer(60000,function(){
                    console.log("Done!");
                    var score = 0;
                    for (var i = 0; i<answers.length; i++){
                        if (answers[i]["playerAnswer"] === questions["questions"][i%questions["questions"].length]["answer"]){
                            score = score + 1;
                        }
                    }
                    //$('.main-content').html('<h3><span style="color:red;">Times Up!</span></h3><h2>Score: ' + score + ' out of ' + answers.length + ' answers.</h2>');
                    /* Display finished modal; disable answers; collect answers, and request report*/

                    $('.main-content').html('<h3><span style="color:red;">Times up!</span></h3><form><fieldset><legend>Enter your email address to register and see your results</legend><div class="row"><div class="large-12 columns"><label>Email</label><input class="player-email" type="email" placeholder="example@me.com" required><a href="#" class="button submit-results">Register</a></div></div></fieldset></form>');
                });
            }

            // Show the tour
            $(document).foundation('joyride','start', {'postRideCallback': playGame});
            // After the final modal, start the game

        });

        $(document).on('click touchstart', '.answer-block', function() {
            // Store the answer
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
    });

    /* Game */
    // Show "Ready", "Start", then start the game.


    // Helper functions
    

    function renderBaseGameTemplate(){
        // Compiled via doT; fix this.
        //var out = '<div class="game"> <div class="question-block"> <div id="timer" class="timer"><div class="progress radius"><span id="timer-region" class="meter"></span></div></div> <hr> <div id="question" class="question"><h3><pre></pre></h3></div> <div class="notifications"></div> </div> <div id="answers" class="answers"> <div class="answer-block">Answer 1</div> <div class="answer-block">Answer 2</div> <div class="answer-block">Answer 3</div> <div class="answer-block">Answer 4</div> </div></div> <!-- Joyride Demo --> <ol class="joyride-list" data-joyride> <li data-button="Next"> <p>Welcome to the word association game!</p><p> We\'re going to walk you through an example question so you know what to expect.</p> </li> <li data-id="question" data-text="Next"> <p>A word, phrase, or snippet of code will show up here.</p> </li> <li data-id="answers" data-text="Next" data-options="nubPosition:left;"> <p>You\'ll select the word over here that is most associated with it.</p> <p>Since <code>if</code> statements are used to check logic an execute some block of code conditionally, <code>conditional</code> is the right answer!</p> </li> <li data-id="timer" data-button="Next"> <p>Answer carefully, wrong answers will hurt your score, but answer quickly, becuase the more answers you get right before this timer runs out, the higher your score!</p> </li> <li data-button="Start the game!"> <p>Questions will be a mix from several different categories. You may be asked to match a snipped of code to the language it\'s written in, match some real world scenario to the data structure that naturally represents it, or identify an object oriented design principle.</p> <p>Competition will be fierce, and the game moves fast, so take a moment, focus, and get ready to start!</p> </li> </ol>';
        var out = '<div class="game"> <div class="question-block"> <div id="timer" class="timer"><div class="progress radius"><span id="timer-region" class="meter"></span></div></div> <hr> <div id="question" class="question"><h3><pre></pre></h3></div> <div class="notifications"></div> </div> <div id="answers" class="answers"> <div class="answer-block">Answer 1</div> <div class="answer-block">Answer 2</div> <div class="answer-block">Answer 3</div> <div class="answer-block">Answer 4</div> </div></div> <!-- Joyride Demo --> <ol class="joyride-list" data-joyride> <li data-button="Next"> <p>Welcome to the word association game!</p> <p> We\'re going to walk you through an example question so you know what to expect.</p> </li> <li data-id="question" data-text="Next"> <p>A word, phrase, or snippet of code will show up here.</p> </li> <li data-id="answers" data-text="Next"> <p>You\'ll select the word over here that is most associated with it.</p> <p>Since <code>if</code> statements are used to check logic an execute some block of code conditionally, this is the right answer!</p> </li> <li data-id="timer" data-button="Next"> <p>Answer carefully, wrong answers will hurt your score, but answer quickly, becuase the more answers you get right before this timer runs out, the higher your score!</p> </li> <li data-button="Start the game!"> <p>Questions will be a mix from several different categories. You may be asked to match a snipped of code to the language it\'s written in, match some real world scenario to the data structure that naturally represents it, or identify an object oriented design principle.</p> <p>Competition will be fierce, and the game moves fast, so take a moment, focus, and get ready to start!</p> </li> </ol>';
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
