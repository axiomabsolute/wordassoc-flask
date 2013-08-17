from flask import Flask, render_template, request, session, abort, jsonify
from random import sample
from questions import question_bank
app = Flask(__name__)

# Sample test data
result = {"reports":[
    {
        "label": "Average time per question",
        "value": 2.4,
        "type": "basic"
    },
    {
        "label": "Percent of questions correct",
        "value": "80%",
        "type": "basic"
    }
]}

questions = {
    "questions": [
        {
            "question": "HEAD~2",
            "options": sample(["git", "Java", "C#", "Python"],4),
            "answer": "git"
        } for x in range(19)
    ]
}

questions["questions"].append({
            "question": "test",
            "options": ["git", "Java", "C#", "Python"],
            "answer": "git"
        })


def generateTechAnswers(question):
    question["options"] = sample(question_bank["technologies"],4)
    if question["question_answer"] in question["options"]:
        question["options"].remove(question["question_answer"])
    question["options"] = question["options"][:3]

def generateOODConceptAnswers():
    question["options"] = sample(question_bank["ood-concepts"],4)
    if question["question_answer"] in question["options"]:
        question["options"].remove(question["question_answer"])
    question["options"] = question["options"][:3]

def generateDataStructAnswers():
    question["options"] = question_bank["data-structures"]

def generateAlgorithmAnswers():
    question["options"] = question_bank["algorithm-types"]

def generateGeneralAnswers():
    question["options"] = sample(question_bank["general-programming-principles"],4)
    if question["question_answer"] in question["options"]:
        question["options"].remove(question["question_answer"])
    question["options"] = question["options"][:3]

mapOfQuestionTypesToAnswerGenerationMethods = {
    "snippetToTech" : generateTechAnswers,
    "everydayDataStructs" : generateDataStructAnswers,
    "snippetToOODConcept" : generateOODConceptAnswers,
    "algorithmToType" : generateAlgorithmAnswers,
    "generalProgrammingPrinciples" : generateGeneralAnswers
}

supportedTechs = [
    {
        "technology": "git",
        "color": "#000000",
        "background_color": "#FF0000"
    } for x in range(14)
]
supportedTechs.append(
    {
        "technology": "somethingElse",
        "color": "#000000",
        "background_color": "#00FF00"
    })

technologies = ("git")

# Routes
@app.route('/')
def login():
    return render_template('login.html', is_ajax=is_xmlhttp_request(request.headers))

@app.route('/techs')
def techs():
    email = request.args.get('email', None)
    if email:
        session['email'] = email
        technologies=getTechsForUser(email)
    return render_template('techs.html', supportedTechs=supportedTechs, technologies=technologies, is_ajax=is_xmlhttp_request(request.headers))

@app.route('/game')
def play_game():
    techs = request.args.get('techs', None)
    if techs:
        session['techs'] = techs
    questions = generateQuestions(techs)
    return jsonify(questions)
    #return render_template('game.html', is_ajax=is_xmlhttp_request(request.headers))

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
    return questions

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test"
    app.run()
