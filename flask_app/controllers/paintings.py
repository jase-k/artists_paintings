from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.painting import Painting

@app.route('/paintings/add')
def addPaintingPage():
    return render_template('add_edit_painting.html')

@app.route('/paintings/add/new', methods = ["POST"])
def addPainting():
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity' : request.form['quantity'],
        'artist_id': session['artist_id']
    }
    session['title'] =data['title']
    session['description'] = data['description']
    session['price'] = data['price']
    session['quantity'] = data['quantity']

    id = Painting.addPainting(data)

    if id:
        session['title'] = ''
        session['description'] = ''
        session['price'] = ''
        session['quantity'] = ''

        return redirect(f'/artists/{session["artist_id"]}')
    else:
        return redirect('/paintings/add')
