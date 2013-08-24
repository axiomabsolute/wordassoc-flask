from flask import Flask, render_template, request, session, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from Models import db, Player, Question, Answer, Game
from utilities import question_bank, technologies, generateQuestions, is_xmlhttp_request
from reports import calculateAccuracyByTech, calculateCorrectByCategory, getLeaderboard
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
    question_list = generateQuestions(techs)
    questions = {"questions":question_list}
    return jsonify(questions)

@app.route('/result', methods=["POST"])
def result():
    data = json.loads(request.data)
    answers = data["answers"]
    email = data["player"]
    game = Game(person_id=email)
    # Create player if doesn't exit
    player = Player.query.get(email) or Player(email=email)
    # Create Answer fields
    total_answers = 0
    correct_answers = 0
    for a in answers:
        question = Question.query.get(a["question"])
        correct_answer = a["playerAnswer"]==question.correctAnswer
        answer = Answer(playerAnswer=a["playerAnswer"], player=Player.query.get(email), question=question, game=game, correct=correct_answer)
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
    accuracyByTech = calculateAccuracyByTech(game.answers)
    accuracyByQuestionType = calculateCorrectByCategory(game.answers)
    return render_template('result.html', total_answers = total_answers, correct_answers = correct_answers, game_score=game.score, standing=standing, total_games=total_games,accuracyByTech=accuracyByTech, accuracyByCategory=accuracyByQuestionType)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', leaderboard=getLeaderboard(Game.query.all()))    

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    Question.loadQuestionsIntoDb(question_bank['questions'])
    app.debug = True
    app.secret_key = "test"
    app.run()

