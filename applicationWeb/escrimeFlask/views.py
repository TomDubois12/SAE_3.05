from .app import app
from flask import render_template, request
#from .models import *


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

@app.route('/profil')
def profil():
    return render_template('profil.html',
                           title='Mon profil')

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
                           title='Classement_National')

@app.route('/archives')
def archives():
    return render_template('archives.html',
                           title='Archives')

@app.route('/archives_nc')
def archivesNC():
    return render_template('archives_nc.html',
                           title='Archives_NonConnecté')

@app.route('/options_competitions')
def options_competitions():
    return render_template('options_competitions.html',
                           title='Options_Compétitions')

@app.route('/resultats')
def resultats():
    return render_template('resultats.html',
                           title='Résultats')

@app.route('/verifInscription')
def verifInscription():
     if estDansBDNational(int(request.args.get("nbLicence"))):
        print(estDansBDNational(int(request.args.get("nbLicence"))))
        if insertTireurDansCompetition(str(request.args.get("nom")), str(request.args.get("prenom")),  int(request.args.get("nbLicence")), str(request.args.get("naissance")), str(request.args.get("club")), int(request.args.get("compet")), str(request.args.get("role"))):
            return render_template('inscription.html',
                            title='Inscription',
                            competitions=inscriptionOuverte(),
                            popup3=True)
        else:
            return render_template('inscription.html',
                            title='Inscription',
                            competitions=inscriptionOuverte(),
                            popup2=True)
     else:
        return render_template('inscription.html',
                           title='Inscription',
                           popup=True,
                           competitions=inscriptionOuverte(),
                           nbLicence=request.args.get("nbLicence"))


@app.route('/verifConnexionEscrimeur')
def verifConnexionEscrimeur():
    if estDansBDNational(int(request.args.get("nbLicense"))):
        concoursTireur = concourtInscritLicenceTireur(int(request.args.get("nbLicense")))
        concoursArbitre = concourtInscritLicenceArbitre(int(request.args.get("nbLicense")))
        concours=concoursTireur+concoursArbitre

        if concours!=[]:
            return render_template('connexion_escrimeur.html',
                               title='Connexion_escrimeur',
                               affichageConcours=True,
                               concoursTireur=concoursTireur,
                               concoursArbitre=concoursArbitre)
        
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
