from flask import Flask, render_template, request, session, abort
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

technologies = [
    {
        "technology": "git",
        "color": "#000000",
        "background_color": "#FF0000",
        "selected": 15%(x+1)==0
    } for x in range(15)
]

# Routes
@app.route('/')
def login():
    return render_template('login.html', is_ajax=is_xmlhttp_request(request.headers))

@app.route('/techs')
def techs():
    email = request.args.get('email', None)
    if email:
        session['email'] = email
    return render_template('techs.html', technologies=technologies, is_ajax=is_xmlhttp_request(request.headers))

@app.route('/game')
def play_game():
    techs = request.args.get('techs', None)
    print(render_template('game.html', is_ajax=is_xmlhttp_request(request.headers)))
    return render_template('game.html', is_ajax=is_xmlhttp_request(request.headers))

@app.route('/result')
def result():
    return render_template('result.html', result=result, is_ajax=is_xmlhttp_request(request.headers))

"""
Check in the headers dict for the 'X-Requested-With' key, which is added with jQuery AJAX requests, and
if the value is XMLHttpRequest, indicating an HTTML request.
"""
def is_xmlhttp_request(headers):
    return (headers.has_key("X-Requested-With") and headers["X-Requested-With"] == "XMLHttpRequest")

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test"
    app.run()
