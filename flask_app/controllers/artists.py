from flask_app import app

@app.route('/')
def mainPage():
    return 'Hello World'