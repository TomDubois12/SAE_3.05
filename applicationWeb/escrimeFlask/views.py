from .app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('lancement.html',
                           title='Lancement')

@app.route('/information')
def information():
    return render_template('information.html',
                           title='Information')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html',
                           title='Inscription')

@app.route('/connexion_organisateur')
def connexion_organisateur():
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')

@app.route('/accueil')
def accueil():
    return render_template('accueil.html',
                           title='Accueil')