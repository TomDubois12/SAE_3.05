from .app import app
from flask import render_template, request, redirect, url_for
from .models import *

##Fonctions de redirection vers les pages sans connexion

@app.route('/')
def index():
    return render_template('lancement.html',
                           title='Lancement')

@app.route('/information')
def information():
    return render_template('information.html',
                           title='Information')

@app.route('/connexion_escrimeur')
def connexion_escrimeur():
    return render_template('connexion_escrimeur.html',
                           title='Connexion_escrimeur')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html',
                           title='Inscription',
                           competitions=inscriptionOuverte())

@app.route('/connexion_organisateur')
def connexion_organisateur():
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')

@app.route('/archives_nc')
def archivesNC():
    return render_template('archives_nc.html',
                           title='Archives_NonConnecté')

##Fonctions de redirection vers les pages avec connexion

@app.route('/profil/<nbLicense>')
def profil(nbLicense):
    return render_template('profil.html',
                           title='Mon profil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbLicense=nbLicense,
                            informations=getProfil(int(nbLicense)))

@app.route('/accueil/<nbLicense>')
def accueil(nbLicense):
    return render_template('accueil.html',
                           title='Accueil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense)

@app.route('/classement_national/<nbLicense>')
def classement_national(nbLicense):
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense)

@app.route('/archives/<nbLicense>')
def archives(nbLicense):
    return render_template('archives.html',
                           title='Archives',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense,
                           villes=getListeComiteReg(),
                           competitions=getListTournoisAllCLosed(),
                           competitionsParticiper=getTournoisClosedParticiper(int(nbLicense)))

@app.route('/options_competitions/<nbLicense>')
def options_competitions(nbLicense):
    return render_template('options_competitions.html',
                           title='Options_Compétitions',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense,
                           mesCompetitions=getCompetitionParOrga(nbLicense))

@app.route('/resultats/<nbLicense>')
def resultats(nbLicense):
    return render_template('resultats.html',
                           title='Résultats',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense)


##Fonctions de vérification


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

@app.route('/rechercheArchives')
def rechercheArchives():
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    ville=request.args.get("ville")
    nbLicense=request.args.get("nbLicense")
    return redirect(url_for('archives', nbLicense=nbLicense))

@app.route('/rechercheClassement')
def rechercheClassement():
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    nbLicense=request.args.get("nbLicense")
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=nbLicense,
                           classement=getClassementNationnal(arme,sexe,categorie))

