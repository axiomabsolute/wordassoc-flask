from flask import Flask, render_template, request, session, abort, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from Models import db, Player, Question, Answer, Game
from utilities import question_bank, technologies, generateQuestions, is_xmlhttp_request, mapOfQuestionTypesToDisplayName, mapOfQuestionTypesToShortName
from reports import calculateAccuracyByTech, calculateCorrectByCategory, getLeaderboard, countQuestionsByType, calculateCorrect
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_TEAL_URL', 'sqlite:///localdata/local.db')
db.app = app
db.init_app(app)


# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/techs')
def techs():
    resp = render_template('techs.html', supportedTechs=question_bank["technologies"],
            baseTechs=question_bank["base_techs"], technologies=technologies,
            is_ajax=is_xmlhttp_request(request.headers))
    return resp

@app.route('/game')
def play_game():
    techs = request.args.get('techs', None)
    if not techs:
        techs = technologies
    else:
        techs = techs.split(',')
    question_list = generateQuestions(techs)
    questions = {"questions":question_list}
    return jsonify(questions)

@app.route('/timesup')
def game_finished_html():
    return render_template('timesup.html')

@app.route('/baseGameTemplate')
def base_game_html():
    return render_template('game.html')

@app.route('/result', methods=["POST"])
def result():
    data = json.loads(request.data)
    answers = data["answers"]
    email = data["player"]
    game = Game(person_id=email)
    question_table_data = []
    # Create player if doesn't exit
    player = Player.query.get(email) or Player(email=email)
    # Create Answer fields
    total_answers = 0
    correct_answers = 0
    for a in answers:
        question = Question.query.get(a["question"])
        if not question:
            print("ERROR - Missing question : " + str(a["question"]))
            continue
        correct_answer = a["playerAnswer"]==question.correctAnswer
        answer = Answer(playerAnswer=a["playerAnswer"], player=Player.query.get(email), question=question, game=game, correct=correct_answer)
        question_table_data.append({"question": question.text, "answer": question.correctAnswer, "userAnswer": a["playerAnswer"]})
        if correct_answer:
            correct_answers = correct_answers + 1
        total_answers = total_answers + 1
        player.answers.append(answer)
        db.session.add(answer)
    # Calculate the game score
    game.score = score=correct_answers - (0.25 * (total_answers - correct_answers))
    db.session.add(game)
    # Commit to DB
    db.session.commit()
    # Render results
    standing = Game.query.filter(Game.score>game.score).count() + 1
    total_games = Game.query.count()
    questionCountsByType = countQuestionsByType(game.answers, mapOfQuestionTypesToShortName)
    accuracyByTech = calculateAccuracyByTech(game.answers)
    accuracyByQuestionType = calculateCorrectByCategory(game.answers)
    accuracyByLabel = calculateCorrect(game.answers, mapOfQuestionTypesToShortName)
    visualization_data = {"total_answers": total_answers, "correct_answers": correct_answers, 
            "accuracyByTech": accuracyByTech, "accuracyByCategory": accuracyByQuestionType, "game_score": game.score, 
            "standing": standing, "total_games": total_games, "question_table_data": question_table_data,
            "questionCountsByType": questionCountsByType, "accuracyByLabel": accuracyByLabel}
    return render_template('result.html', total_answers = total_answers, correct_answers = correct_answers,
            game_score=game.score, standing=standing, total_games=total_games,accuracyByTech=accuracyByTech,
            accuracyByCategory=accuracyByQuestionType, questionTableData=question_table_data, 
            mapOfQuestionTypesToDisplayName=mapOfQuestionTypesToDisplayName, visualization_data=json.dumps(visualization_data),
            mapOfQuestionTypesToShortName=mapOfQuestionTypesToShortName, accuracyByLabel=accuracyByLabel)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', leaderboard=getLeaderboard(Game.query.all()))

@app.route('/leaderboard2')
def leaderboard2():
    return render_template('leaderboard.html', leaderboard=getLeaderboard(Game.query.all()))

@app.route('/result_debug')
def result_debug():
    """
    Get's the highest scoring game for the user and renders the results.  Used only for debugging (to prevent giving away other people's information)
    """
    if not app.debug:
        abort(403)
    user_email = request.args.get('user', None)
    if not user_email:
        abort(400)
    game = Game.query.filter_by(person_id=user_email).order_by(Game.score).first()
    if not game:
        abort(404)
    gameId = game.id
    answers = db.session.query(Answer).filter(Answer.game_id==gameId).join(Question).all()
    # Various default fields required for the template
    total_answers = 0
    correct_answers = 0
    accuracyByTech = 0
    accuracyByQuestionType = 0
    question_table_data = []
    questionCountsByType = {};
    game_score = game.score
    standing = Game.query.filter(Game.score>game.score).count()+1
    total_games = Game.query.count()
    for a in answers:
        question_table_data.append({"question": a.question_id, "answer": a.question.correctAnswer, "userAnswer": a.playerAnswer})
        if a.correct:
            correct_answers = correct_answers + 1
        total_answers = total_answers + 1
    questionCountsByType = countQuestionsByType(answers, mapOfQuestionTypesToShortName)
    accuracyByTech = calculateAccuracyByTech(answers)
    accuracyByQuestionType = calculateCorrectByCategory(answers)
    accuracyByLabel = calculateCorrect(answers, mapOfQuestionTypesToShortName)
    visualization_data = {"total_answers": total_answers, "correct_answers": correct_answers, 
            "accuracyByTech": accuracyByTech, "accuracyByCategory": accuracyByQuestionType, "game_score": game_score, 
            "standing": standing, "total_games": total_games, "question_table_data": question_table_data,
            "questionCountsByType": questionCountsByType, "accuracyByLabel": accuracyByLabel}
    return render_template('result.html', total_answers = total_answers, correct_answers = correct_answers,
            game_score=game.score, standing=standing, total_games=total_games,accuracyByTech=accuracyByTech,
            accuracyByCategory=accuracyByQuestionType, questionTableData=question_table_data, 
            mapOfQuestionTypesToDisplayName=mapOfQuestionTypesToDisplayName, debugMode=True, visualization_data=json.dumps(visualization_data),
            mapOfQuestionTypesToShortName=mapOfQuestionTypesToShortName, accuracyByLabel=accuracyByLabel)

        

def reloadDb():
    print("Dropping all dables.")
    db.drop_all()
    db.session.commit()
    print("Creating tables for each model");
    db.create_all()
    db.session.commit()
    print("Syncing questions")
    Question.loadQuestionsIntoDb(question_bank['questions'])

def syncQuestions():
    Question.loadQuestionsIntoDb(question_bank['questions'])

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    Question.loadQuestionsIntoDb(question_bank['questions'])
    app.debug = True
    app.secret_key = "test"
    app.run()

