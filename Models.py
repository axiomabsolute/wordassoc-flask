from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model classes
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Name %r>" % self.name

class Question(db.Model):
    text = db.Column(db.String(255), primary_key=True)
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
    question = db.Column(db.Integer, db.ForeignKey('question.text'))
    user = db.Column(db.String(255), db.ForeignKey('user.email'))
    userAnswer = db.Column(db.String(255))
    

    def __init__(self, question, userAnswer, user):
        self.question = question
        self.userAnswer = userAnswer
        self.user = user

