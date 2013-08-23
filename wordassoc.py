from flask import Flask, render_template, request, session, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from random import sample, shuffle, choice
from questions import question_bank
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_TEAL_URL', 'sqlite:///localdata/local.db')
db = SQLAlchemy(app)

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

# Routes
@app.route('/')
def login():
    return render_template('login.html', is_ajax=is_xmlhttp_request(request.headers))

@app.route('/techs')
def techs():
    print("Here?")
    email = request.args.get('email', None)
    print("email: " + str(email))
    resp = render_template('techs.html', supportedTechs=question_bank["technologies"], 
            baseTechs=question_bank["base_techs"], technologies=technologies, 
            is_ajax=is_xmlhttp_request(request.headers))
    return resp

@app.route('/game')
def play_game():
    print("Make it to the game method.")
    print(request.cookies.get("user-email"))
    techs = request.args.get('techs', None)
    if not techs:
        techs = technologies
    question_list = generateQuestions(techs)
    questions = {"questions":question_list}
    return jsonify(questions)

@app.route('/result')
def result():
    answers = request.args.get('answers', None)
    return render_template('result.html', result=result, is_ajax=is_xmlhttp_request(request.headers))

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

# Model classes
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Name %r>" % self.name

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    correctAnswer = db.Column(db.String(255))
    questionType = db.Column(db.String(255))

    def __init__(self, text, correctAnswer, questionType):
        self.text = text
        self.correctAnswer = correctAnswer
        self.questionType = questionType

    @staticmethod
    def loadQuestionsIntoDb(questions):
        if len(Question.query.all()) != len(questions):
            print("Question table not synced: " + str(len(Question.query.all())) + " vs. " + str(len(questions)))
            print("Cleaning out question table")
            for old_q in Question.query.all():
                db.session.delete(old_q)
            db.session.commit()
            print("Adding new questions")
            for question in questions:
                db.session.add(Question(question['question'],question['answer'],question['question_type']))
            print("Committing questions")
            db.session.commit()
            print("Questions synced")

class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)

    def __init__(self, email):
        self.email = email

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), db.ForeignKey('user.email'))

    def __init__(self, user):
        self.user = user

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    user = db.Column(db.String(255), db.ForeignKey('user.email'))
    userAnswer = db.Column(db.String(255))
    

    def __init__(self, question, userAnswer, user):
        self.question = question
        self.userAnswer = userAnswer
        self.user = user

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    Question.loadQuestionsIntoDb(question_bank['questions'])
    app.debug = True
    app.secret_key = "test"
    app.run()

