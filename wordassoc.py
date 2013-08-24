from flask import Flask, render_template, request, session, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from random import sample, shuffle, choice
from questions import question_bank
from Models import db, User, Question, Answer, Game
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_TEAL_URL', 'sqlite:///localdata/local.db')
db.app = app
db.init_app(app)

# Helper methods
def generateTechAnswers(question):
    options = sample(question_bank["technologies"],4)
    if question["answer"] in options:
        options.remove(question["answer"])
    options = options[:3]
    options.append(question["answer"])
    shuffle(options)
    return options

def generateOODConceptAnswers(question):
    options = sample(question_bank["ood-concepts"],4)
    if question["answer"] in options:
        options.remove(question["answer"])
    options = options[:3]
    options.append(question["answer"])
    shuffle(options)
    return options

def generateDataStructAnswers(question):
    return question_bank["data-structures"]

def generateAlgorithmAnswers(question):
    return question_bank["algorithm-types"]

def generateGeneralAnswers(question):
    options = sample(question_bank["general-programming-principles"],4)
    if question["answer"] in options:
        options.remove(question["answer"])
    options = options[:3]
    options.append(question["answer"])
    shuffle(options)
    return options

def generateAnswers(question):
    return mapOfQuestionTypesToAnswerGenerationMethods[question["question_type"]](question)

mapOfQuestionTypesToAnswerGenerationMethods = {
    "snippetToTech" : generateTechAnswers,
    "everydayDataStructs" : generateDataStructAnswers,
    "snippetToOODConcept" : generateOODConceptAnswers,
    "algorithmToType" : generateAlgorithmAnswers,
    "generalProgrammingPrinciples" : generateGeneralAnswers
}

technologies = ("git","java","javascript","python")

"""
Check in the headers dict for the 'X-Requested-With' key, which is added with jQuery AJAX requests, and
if the value is XMLHttpRequest, indicating an HTTML request.
"""
def is_xmlhttp_request(headers):
    return (headers.has_key("X-Requested-With") and headers["X-Requested-With"] == "XMLHttpRequest")

def getTechsForUser(email):
    return technologies

def generateQuestions(techs):
    """
    This is really not a great way of generating the questions.  The likelihood of a repeat question is very
    high, but the options will likely be different at least.  Might be a good idea to sample + filter first,
    then randomly select to fill up the space.
    """
    questions = []
    questions_sample = sample(question_bank["questions"], 60)
    for q in questions_sample:
        if q["question_type"] == "snippetToTech":
            if len(techs)<4:
                continue
            if q["answer"] not in techs:
                continue
        q = q.copy()
        q["options"] = generateAnswers(q)
        questions.append(q)
    # Make sure we get at least 60 questions.
    while len(questions) < 60:
        question = choice(question_bank["questions"])
        if question["question_type"] == "snippetToTech":
            if len(techs)<4:
                continue
            if question["answer"] not in techs:
                continue
        question = question.copy()
        question["options"] = generateAnswers(question)
        questions.append(question)
    return questions

# Routes
@app.route('/')
def login():
    return render_template('login.html', is_ajax=is_xmlhttp_request(request.headers))

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
    email = data["user"]
    # Generate game
    game = Game()
    db.session.add(game)
    # Create user if doesn't exit
    user = User.query.filter_by(email=email) or User(email=email)
    # Create Answer fields
    for a in answers:
        question = Question.query.get(a["question"])
        answer = Answer(userAnswer=a["userAnswer"], user=User.query.get(email), question=question, game=game, correct=(a["userAnswer"]==question.correctAnswer))
    # Commit to DB
    db.session.commit()
    # Render results
    total_answers = len(Answer.query.filter_by(game=game).all())
    correct_answers = len(Answer.query.filter_by(game=game).filter_by(correct=True).all())
    print("Games: " + str(len(Game.query.all())))
    return render_template('result.html', total_answers = total_answers, correct_answers = correct_answers)

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    Question.loadQuestionsIntoDb(question_bank['questions'])
    app.debug = True
    app.secret_key = "test"
    app.run()

