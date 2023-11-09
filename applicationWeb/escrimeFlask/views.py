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

##Fonctions de redirection vers les pages avec connexion

@app.route('/profil/<nbLicense>&<nbCompet>')
def profil(nbLicense,nbCompet):
    return render_template('profil.html',
                           title='Mon profil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbLicense=int(nbLicense),
                            nbCompet=int(nbCompet),
                            informations=getProfil(int(nbLicense)),
                            stats=getStatistique(int(nbLicense)))

@app.route('/accueil/<nbLicense>&<nbCompet>')
def accueil(nbLicense,nbCompet):
    return render_template('accueil.html',
                           title='Accueil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbCompet=int(nbCompet),
                           nbLicense=int(nbLicense),
                           nomCompet=getInfoCompetition(int(nbCompet))[0][1],
                           nombreCompet=len(getTournoisClosedParticiper(int(nbLicense))))

@app.route('/classement_national/<nbLicense>&<nbCompet>')
def classement_national(nbLicense,nbCompet):
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbCompet=int(nbCompet),
                           nbLicense=int(nbLicense))

@app.route('/archives/<nbLicense>&<nbCompet>')
def archives(nbLicense,nbCompet):
    return render_template('archives.html',
                           title='Archives',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           nbCompet=int(nbCompet),
                           villes=getListeComiteReg(),
                           competitions=getListTournoisAllCLosed(),
                           competitionsParticiper=getTournoisClosedParticiper(int(nbLicense)))

@app.route('/options_competitions/<nbLicense>')
def options_competitions(nbLicense):
    return render_template('options_competitions.html',
                           title='Options_Compétitions',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           mesCompetitions=getCompetitionParOrga(nbLicense),
                           tournoisArchiver=getListIdCompetitionTournoisClosed(),
                           tournoisLancer=getListIdCompetitionTournoisLancer())

@app.route('/creation_competition/<nbLicense>')
def creation_competition(nbLicense):
    return render_template('creation_competition.html',
                           title='Création_Compétition',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           villes=getListeComiteReg())

@app.route('/resultats/<nbLicense>&<nbCompet>')
def resultats(nbLicense,nbCompet):
    return render_template('resultats.html',
                           title='Résultats',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbCompet=int(nbCompet),
                           nbLicense=int(nbLicense))


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
        concoursTireur = concourtNonFinitInscritTireur(int(request.args.get("nbLicense")))
        concoursArbitre = concourtNonFinitInscritArbitre(int(request.args.get("nbLicense")))
        concours=concoursTireur+concoursArbitre

        if concours!=[]:
            return render_template('connexion_escrimeur.html',
                               title='Connexion_escrimeur',
                               affichageConcours=True,
                               concoursTireur=concoursTireur,
                               concoursArbitre=concoursArbitre,
                               nbLicense=request.args.get("nbLicense"))
        
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
        return redirect('options_competitions/'+str(request.args.get("nblicense")))
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
    nbCompet=request.args.get("nbCompet")
    return render_template('archives.html',
                           title='Archives',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                            nbCompet=int(nbCompet),
                           villes=getListeComiteReg(),
                           competitions=trieArchive(str(arme),str(sexe),str(categorie),str(ville)),
                           competitionsParticiper=getTournoisClosedParticiper(int(nbLicense)))

@app.route('/rechercheArchivesNC')
def rechercheArchivesNC():
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    ville=request.args.get("ville")
    return render_template('archives_nc.html',
                           title='Archives',
                           villes=getListeComiteReg(),
                           competitions=trieArchive(str(arme),str(sexe),str(categorie),str(ville)))


@app.route('/rechercheClassement')
def rechercheClassement():
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    nbLicense=request.args.get("nbLicense")
    nbCompet=request.args.get("nbCompet")
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           nbCompet=int(nbCompet),
                           classement=getClassementNationnal(arme,sexe,categorie))

@app.route('/validationConnexion')
def validationConnexion():
    nbCompet=request.args.get("compet")
    nbLicense=request.args.get("nbLicense")
    return redirect('accueil/'+str(nbLicense)+'&'+str(nbCompet))


@app.route('/creationCompetition')
def creationCompetition():
    nom=request.args.get("nom")
    lieu=request.args.get("ville")
    date=request.args.get("date")
    categorie=request.args.get("categorie")
    sexe=request.args.get("sexe")
    arme=request.args.get("arme")
    coeff=request.args.get("coeff")
    nbLicense=request.args.get("nbLicense")
    createCompetition(nom,lieu,categorie,sexe,arme,coeff,date,nbLicense)
    return redirect('options_competitions/'+str(nbLicense))


@app.route('/boutonLancer')
def boutonLancer():
    lancerCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))

@app.route('/boutonArchiver')
def boutonArchiver():
    archiverCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))