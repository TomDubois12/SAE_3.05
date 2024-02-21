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
                           competitions=inscriptionOuverteSolo())
    
@app.route('/inscriptionSoloEquipe')
def inscriptionSoloEquipe():
    return render_template('inscriptionSoloEquipe.html',
                           title='Inscription_Solo_Equipe')

@app.route('/inscription_arbitre')
def inscription_arbitre():
    return render_template('inscription_arbitre.html',
                           title='Inscription Arbitre',
                           competitions=inscriptionOuverteEquipe())

@app.route('/inscription_equipe')
def inscription_equipe():
    return render_template('inscription_equipe.html',
                           title='Inscription Equipe',
                           competitions=inscriptionOuverteEquipe())

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

@app.route('/infoCompetition/<nbLicense>&<nbCompet>')
def infoCompetition(nbLicense,nbCompet):
    if isCompetitionEquipe(int(nbCompet)):
        participants=getEquipeDansCompetition(int(nbCompet))
    else:
        participants=getNomTireurs(int(nbCompet))
    return render_template('infoCompetition.html',
                           title='Info_Competition',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbLicense=int(nbLicense),
                            participants=participants,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)))

@app.route('/creation_competition/<nbLicense>')
def creation_competition(nbLicense):
    return render_template('creation_competition.html',
                           title='Création_Compétition',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           villes=getListeComiteReg())

@app.route('/resultats/<nbLicense>&<nbCompet>')
def resultats(nbLicense,nbCompet):
    nbPartipant = getNbParticipant(int(nbCompet))
    nbTotalPhase = nbPartipant
    
    trouve = False
    i=0
    while not trouve:
        if nbPartipant <= 2**i:
            nbTotalPhase = i
            trouve = True
        i+=1

    listArbitres= getNumeroLicenceArbitres(int(nbCompet))
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    lancer=False
    if int(nbCompet) in getListIdCompetitionTournoisLancer():
        lancer=True
        # print('\033[93m' + str(lancer) + '\033[0m')
    if int(nbCompet) in getListIdCompetitionTournoisClosed():
        lancer=True
        # print('\033[93m' + str(lancer) + '\033[0m')
    # print('\033[93m' + str(lancer) + '\033[0m')
    print('\033[92m' + str(classementFinale(int(nbCompet),getNbPhase(int(nbCompet)))) + '\033[0m')
    if lancer:
        if int(nbLicense) in listArbitres:
            return render_template('resultats.html',
                            title='Résultats',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=InfosPouleNumLicenceArbitre(int(nbCompet),int(nbLicense)),
                            isArbitre=True,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=getNomPrenomMatchElimination(int(nbCompet)),
                            scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                            lancer=lancer,
                            classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                            nbTotalPhase=nbTotalPhase)
        
        elif estParticipant(int(nbLicense), int(nbCompet)):
            return render_template('resultats.html',
                                title='Résultats',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                participants=InfosPouleNumLicence(int(nbCompet),int(nbLicense)),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=getNomPrenomMatchElimination(int(nbCompet)),
                                scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                                lancer=lancer,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                classementPerso=monClassementAMoi(int(nbCompet), int(nbLicense),getNbPhase(int(nbCompet))),
                                joueur=True,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                nbTotalPhase=nbTotalPhase)
        else:
            return render_template('resultats.html',
                                title='Résultats',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                participants=InfosPouleSansLicence(int(nbCompet)),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=getNomPrenomMatchElimination(int(nbCompet)),
                                scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                                lancer=lancer,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                nbTotalPhase=nbTotalPhase)
    else:
        return render_template('resultats.html',
                            title='Résultats',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=[],
                            isArbitre=False,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=getNomPrenomMatchElimination(int(nbCompet)),
                            scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                            lancer=lancer,
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                            nbTotalPhase=nbTotalPhase)

@app.route('/resultats_equipe/<nbLicense>&<nbCompet>')
def resultats_equipe(nbLicense,nbCompet):
    listArbitres= getNumeroLicenceArbitres(int(nbCompet))
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    lancer=False
    if int(nbCompet) in getListIdCompetitionTournoisLancer():
        lancer=True
        # print('\033[93m' + str(lancer) + '\033[0m')
    if int(nbCompet) in getListIdCompetitionTournoisClosed():
        lancer=True
        # print('\033[93m' + str(lancer) + '\033[0m')
    # print('\033[93m' + str(lancer) + '\033[0m')
    print('\033[92m' + str(classementFinale(int(nbCompet),getNbPhase(int(nbCompet)))) + '\033[0m')
    if lancer:
        if int(nbLicense) in listArbitres:
            return render_template('resultats_equipe.html',
                            title='Résultats Equipe',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=InfosPouleNumLicenceArbitre(int(nbCompet),int(nbLicense)),
                            isArbitre=True,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=getNomPrenomMatchElimination(int(nbCompet)),
                            scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                            lancer=lancer,
                            classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))))
        
        elif estParticipant(int(nbLicense), int(nbCompet)):
            return render_template('resultats_equipe.html',
                                title='Résultats Equipe',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                participants=InfosPouleNumLicence(int(nbCompet),int(nbLicense)),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=getNomPrenomMatchElimination(int(nbCompet)),
                                scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                                lancer=lancer,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                classementPerso=monClassementAMoi(int(nbCompet), int(nbLicense),getNbPhase(int(nbCompet))),
                                joueur=True,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))))
        else:
            return render_template('resultats_equipe.html',
                                title='Résultats Equipe',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                participants=InfosPouleSansLicence(int(nbCompet)),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=getNomPrenomMatchElimination(int(nbCompet)),
                                scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                                lancer=lancer,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))))
    else:
        return render_template('resultats_equipe.html',
                            title='Résultats Equipe',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=[],
                            isArbitre=False,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=getNomPrenomMatchElimination(int(nbCompet)),
                            scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                            lancer=lancer,
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))))

##Fonctions de vérification

@app.route('/verifInscription')
def verifInscription():
     if estDansBDNational(int(request.args.get("nbLicence"))):
        print(estDansBDNational(int(request.args.get("nbLicence"))))
        if insertTireurDansCompetition(int(request.args.get("nbLicence")), int(request.args.get("compet")), str(request.args.get("role"))):
            return render_template('inscription.html',
                            title='Inscription',
                            competitions=inscriptionOuverteSolo(),
                            popup3=True)
        else:
            return render_template('inscription.html',
                            title='Inscription',
                            competitions=inscriptionOuverteSolo(),
                            popup2=True)
     else:
        return render_template('inscription.html',
                           title='Inscription',
                           popup=True,
                           competitions=inscriptionOuverteSolo(),
                           nbLicence=request.args.get("nbLicence"))
        
@app.route('/verifInscriptionEquipe')
def verifInscriptionEquipe():
    if estOrganisateur(int(request.args.get("nbLicence"))):
        if insererEquipeDansCompetition(int(request.args.get("compet")), str(request.args.get("nomEquipe")), int(request.args.get("nbLicence"))):
            idEquipe=getIdEquipeByNomEquipeAndCompetition(str(request.args.get("nomEquipe")), int(request.args.get("compet")))
            insererTireurDansEquipe(idEquipe, [int(request.args.get("titulaire1")), int(request.args.get("titulaire2")), int(request.args.get("titulaire3")), int(request.args.get("remplacant"))])
            return render_template('inscription_equipe.html',
                            title='Inscription Equipe',
                            competitions=inscriptionOuverteEquipe(),
                            popup3=True)
        else:
            return render_template('inscription_equipe.html',
                            title='Inscription Equipe',
                            competitions=inscriptionOuverteEquipe(),
                            popup2=True)
    else:
        return render_template('inscription_equipe.html',
                           title='Inscription Equipe',
                           popup=True,
                           competitions=inscriptionOuverteEquipe(),
                           nbLicence=request.args.get("nbLicence"))
        
@app.route('/verifInscriptionEquipe')
def verifInscriptionEquipe():
    if estOrganisateur(int(request.args.get("nbLicence"))):
        if insererEquipeDansCompetition(int(request.args.get("compet")), str(request.args.get("nomEquipe")), int(request.args.get("nbLicence"))):
            insererTireurDansEquipe(request.args.get("compet"), [request.args.get("titulaire1"), request.args.get("titulaire2"), request.args.get("titulaire3"), request.args.get("remplacant")])
            return render_template('inscription_equipe.html',
                            title='Inscription Equipe',
                            competitions=inscriptionOuverteEquipe(),
                            popup3=True)
        else:
            return render_template('inscription_equipe.html',
                            title='Inscription Equipe',
                            competitions=inscriptionOuverteEquipe(),
                            popup2=True)
    else:
        return render_template('inscription_equipe.html',
                           title='Inscription Equipe',
                           popup=True,
                           competitions=inscriptionOuverteEquipe(),
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
    
@app.route('/consulterArchive')
def consulterArchive():
    nbLicense = request.args.get("nbLicense")
    nbCompet = request.args.get("nbCompet")
    ancienNbCompet = request.args.get("ancienNbCompet")
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    return render_template('resultats.html',
                                title='Résultats',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                participants=InfosPouleSansLicence(int(nbCompet)),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=getNomPrenomMatchElimination(int(nbCompet)),
                                scores=getListeToucheByListLicence(licence, int(getNbPhase(int(nbCompet))), int(nbCompet)),
                                lancer=True,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                ancienNbCompet=ancienNbCompet)

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
    typeCompetition=request.args.get("typeCompetition")
    createCompetition(nom,lieu,categorie,sexe,arme,coeff,date,nbLicense,typeCompetition)
    return redirect('options_competitions/'+str(nbLicense))


@app.route('/boutonLancer')
def boutonLancer():
    lancerCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))

@app.route('/boutonArchiver')
def boutonArchiver():
    archiverCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.form.get('data')
    nbLicenceTireur = request.form.get('nbLicenceTireur')
    nbLicenceTireurAdverse = request.form.get('nbLicenceTireurAdverse')
    numCompetition = request.form.get('numCompetition')
    nbPhase = request.form.get('nbPhase')
    setToucherDonneTireur(int(nbLicenceTireur), int(nbLicenceTireurAdverse), int(data), int(numCompetition), int(nbPhase))
    return redirect('resultats/'+str(nbLicenceTireur)+'&'+str(numCompetition))


@app.route('/genererEliminations', methods=['POST'])
def genererEliminations():
    nbCompet = int(request.form.get('nbCompet'))
    nbPhase = int(request.form.get('nbPhase'))
    nbLicense = int(request.form.get('nbLicense'))
    # print('\033[93m' + str(nbCompet) + '\033[0m')
    # print('\033[93m' + str(nbPhase) + '\033[0m')
    genererPhaseEliminations(int(nbCompet), int(nbPhase)+1)
    return redirect('resultats/'+str(nbLicense)+'&'+str(nbCompet))