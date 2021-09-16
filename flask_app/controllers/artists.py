from flask_app.models.painting import Painting
from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.artist import Artist
from flask_app.models.painting import Painting

@app.route('/')
def mainPage():
    return render_template('login.html')

#This route registers an artist and redirects to the artist dashboard to see all paintings
@app.route('/register', methods=['POST'])
def registerArtist():
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password1'],
        "confirm_password" : request.form['password2']
    }

    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']

    if Artist.validateRegistration(data):
        id = Artist.registerArtist(data)
        return redirect(f'/artists/{id}') 
    else:
        return redirect('/')

@app.route('/artists/<int:id>')
def displayDashboard(id):
    if 'artist_id' in session:
        if session['artist_id'] == id:
            artist = Artist.getArtistById(id)
            paintings = Painting.getAllPaintings()
            return render_template('dashboard.html', artist = artist, paintings = paintings)
        else:
            return redirect(f"/artists/{session['artist_id']}")
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def loginArtist():
    #Validate login than redirect to '/artsits/<int:id>
    data = {
        'email' : request.form['email'],
        'password' : request.form['password'] 
    }

    print("Data passed for Validation: ", data)
    id = Artist.validateLogin(data)
    if id:
        return redirect(f'/artists/{id}')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

