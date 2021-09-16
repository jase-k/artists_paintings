from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.painting import Painting

@app.route('/paintings/add')
def addPaintingPage():
    return render_template('add_painting.html')

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

@app.route('/paintings/<int:id>/edit')
def editPaintingPage(id):
    painting = Painting.getPaintingById(id)
    return render_template('edit_painting.html', painting = painting)

@app.route('/paintings/edit', methods = ["POST"])
def updatePainting():
    data = {
        'id': request.form['id'],
        'title': request.form['title'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity' : request.form['quantity'],
        'artist_id': session['artist_id']
    }
    print("Data from edit form: ", data)

    Painting.updatePainting(data)

    return redirect(f'/artists/{data["artist_id"]}')



@app.route('/paintings/<int:id>/delete')
def deletePainting(id):
    pass