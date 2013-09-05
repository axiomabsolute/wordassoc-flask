from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model classes
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return "<Name %r>" % self.name

class Question(db.Model):
    text = db.Column(db.String(255), primary_key=True)
    correctAnswer = db.Column(db.String(255))
    questionType = db.Column(db.String(255))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

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
                q = Question()
                db.session.add(Question(text=question['question'],correctAnswer=question['answer'],questionType=question['question_type'], answers=[]))
            print("Committing questions")
            db.session.commit()
            print("Questions synced")
        else:
            print("Question table appears to be synced at " + str(len(Question.query.all())) + " questions.")

class Player(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    games = db.relationship('Game', backref='player', lazy='dynamic')
    answers = db.relationship('Answer', backref='player', lazy='dynamic')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.String(255), db.ForeignKey(Player.email))
    answers = db.relationship('Answer', backref='game', lazy='dynamic')
    score = db.Column(db.Float)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(255), db.ForeignKey(Question.text))
    player_id = db.Column(db.String(255), db.ForeignKey(Player.email))
    playerAnswer = db.Column(db.String(255))
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    correct = db.Column(db.Boolean)
    
