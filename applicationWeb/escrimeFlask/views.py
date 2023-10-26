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
                           title='Inscription',
                           competitions=inscriptionOuverte())

@app.route('/connexion_organisateur')
def connexion_organisateur():
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')
@app.route('/accueil')
def accueil():
    return render_template('accueil.html',
                           title='Accueil')


    
@app.route('/connexion_escrimeur')
def connexion_escrimeur():
    return render_template('connexion_escrimeur.html',
                           title='Connexion_escrimeur')

  
@app.route('/classement_national')
def classement_national():
    return render_template('classement_national.html',
                           title='Classement National')

    

@app.route('/verifConnexionEscrimeur')
def verifConnexionEscrimeur():
    if estDansBDNational(int(request.args.get("nbLicense"))):
        concours = concourtInscritLicence(int(request.args.get("nbLicense")))
        if concours != []:
            return render_template('connexion_escrimeur.html',
                               title='Connexion_escrimeur',
                               affichageConcours=True,
                               concours=concours)
        else:
            return render_template('connexion_escrimeur.html',
                               title='Connexion_escrimeur',
                               affichageConcours=False,
                               popup=True)
    else:
        return render_template('connexion_escrimeur.html',
                           title='Connexion_escrimeur',
                           affichageConcours=False,
                           popup2=True,
                           nbLicense=request.args.get("nbLicense"))

@app.route('/traitement')
def traitement():
    
    dicoOrganisateur = getOrganisateurClub()
    print(request.args)
    print(dicoOrganisateur)
    print(dicoOrganisateur.keys())
    print()
    if int(request.args.get("nblicense")) in dicoOrganisateur.keys() and dicoOrganisateur[int(request.args.get("nblicense"))] == request.args.get("nomClub"):
        return render_template('connexion_organisateur.html',
                           title='bonne page')
    else:
        return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur',
                           popup=True)

