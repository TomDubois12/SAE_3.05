from .app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('acceuil.html',
                           title='Accueil')

@app.route('/information')
def information():
    return render_template('information.html',
                           title='Information')
    
@app.route('/connexion_organisateur')
def connexion_organisateur():
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')