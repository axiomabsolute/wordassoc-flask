from flask import Flask, render_template, request, session, abort, jsonify
from random import sample, shuffle, choice
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
    app.logger.error("Here?")
    email = request.args.get('email', None)
    app.logger.error("email: " + str(email))
    app.logger.error("Session? " + str(session))
    if email:
        session['email'] = email
   #     technologies=getTechsForUser(email)
    return render_template('techs.html', supportedTechs=question_bank["technologies"], 
            baseTechs=question_bank["base_techs"], technologies=technologies, 
            is_ajax=is_xmlhttp_request(request.headers))

@app.route('/game')
def play_game():
    techs = request.args.get('techs', None)
    if not techs:
        techs = technologies
    question_list = generateQuestions(techs)
    questions = {"questions":question_list}
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

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test"
    app.run()
