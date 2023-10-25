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

@app.route('/inscription')
def inscription():
    return render_template('inscription.html',
                           title='Inscription')