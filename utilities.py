from random import sample, shuffle, choice
from questions import question_bank

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
    "algorithmToBigO" : generateAlgorithmAnswers,
    "generalProgrammingPrinciples" : generateGeneralAnswers
}

mapOfQuestionTypesToDisplayName = {
    "snippetToTech" : "Match code snippet to technology",
    "everydayDataStructs" : "Match everyday application to data structure",
    "snippetToOODConcept" : "Match code snippet to OOD concept",
    "algorithmToBigO" : "Match algorithm to Big-O runtime",
    "generalProgrammingPrinciples" : "Match code snippet to general programming principles"
}

technologies = ()

"""
Check in the headers dict for the 'X-Requested-With' key, which is added with jQuery AJAX requests, and
if the value is XMLHttpRequest, indicating an HTTML request.
"""
def is_xmlhttp_request(headers):
    return (headers.has_key("X-Requested-With") and headers["X-Requested-With"] == "XMLHttpRequest")

def getTechsForPlayer(email):
    return technologies

def generateQuestions(techs):
    """
    This is really not a great way of generating the questions.  The likelihood of a repeat question is very
    high, but the options will likely be different at least.  Might be a good idea to sample + filter first,
    then randomly select to fill up the space.
    """
    questions = []
    questionSet = set()
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
        questionSet.add(q["question"])
    # Make sure we get at least 20 different questions.
    while len(questionSet) < 20:
        question = choice(question_bank["questions"])
        if question["question_type"] == "snippetToTech":
            if len(techs)<4:
                continue
            if question["answer"] not in techs:
                continue
        if question["question"] in questionSet:
            continue
        question = question.copy()
        question["options"] = generateAnswers(question)
        questions.append(question)
        questionSet.add(question["question"])
    # Make sure there's at least 60 questions total
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
    return list(questions)

