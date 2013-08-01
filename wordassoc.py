from flask import Flask, render_template
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
            "options": ["git", "Java", "C#", "Python"],
            "answer": "git"
        }
    ]
}


# Routes
@app.route('/game')
def play_game():
    return render_template('game.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/result')
def result():
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()
