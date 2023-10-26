from .app import app
from flask import render_template, request
from .models import *


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
                        #    competitions=inscriptionOuverte())

@app.route('/connexion_organisateur')
def connexion_organisateur():
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')
@app.route('/accueil')
def accueil():
    return render_template('accueil.html',
                           title='Accueil')

    
    
# @app.route('/traitement')
# def traitement():
    
    # # dicoOrganisateur = getOrganisateurClub()
    # print(request.args)
    # # print(dicoOrganisateur)
    # # print(dicoOrganisateur.keys())
    # print()
    # if int(request.args.get("nblicense")) in dicoOrganisateur.keys() and dicoOrganisateur[int(request.args.get("nblicense"))] == request.args.get("nomClub"):
    #     return render_template('connexion_organisateur.html',
    #                        title='bonne page')
    # else:
    #     return render_template('connexion_organisateur.html',
    #                        title='Connexion_organisateur',
    #                        popup=True)

