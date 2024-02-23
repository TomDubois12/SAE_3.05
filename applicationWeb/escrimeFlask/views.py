from .app import app
from flask import render_template, request, redirect, url_for
from .models import *

##Fonctions de redirection vers les pages sans connexion

@app.route('/')
def index():
    """ Page d'accueil du site

    Returns:
        fonction: affiche la page d'accueil
    """
    return render_template('lancement.html',
                           title='Lancement')

@app.route('/information')
def information():
    """ Page d'information à propos de l'escrime

    Returns:
        fonction: affiche la page d'information
    """
    return render_template('information.html',
                           title='Information')

@app.route('/connexion_escrimeur')
def connexion_escrimeur():
    """ Page de connexion pour les escrimeurs et les arbitres

    Returns:
        fonction: affiche la page de connexion
    """
    return render_template('connexion_escrimeur.html',
                           title='Connexion_escrimeur')

@app.route('/inscription')
def inscription():
    """ Page d'inscription pour les escrimeurs et les arbitres dans une compétition solo

    Returns:
        fonction: affiche la page d'inscription
    """
    return render_template('inscription.html',
                           title='Inscription',
                           competitions=inscriptionOuverteSolo())
    
@app.route('/inscriptionSoloEquipe')
def inscriptionSoloEquipe():
    """ Page pour choisir entre s'inscrire en solo ou en équipe

    Returns:
       fonction : affiche la page d'inscriptionSoloEquipe
    """
    return render_template('inscriptionSoloEquipe.html',
                           title='Inscription_Solo_Equipe')

@app.route('/inscription_arbitre')
def inscription_arbitre():
    """ Page d'inscription pour les arbitres dans une compétition en equipe

    Returns:
        fonction:  affiche la page d'inscription_arbitre
    """
    return render_template('inscription_arbitre.html',
                           title='Inscription Arbitre',
                           competitions=inscriptionOuverteEquipe())

@app.route('/inscription_equipe')
def inscription_equipe():
    """ Page d'inscription pour les escrimeurs dans une compétition en equipe

    Returns:
        fonction: affiche la page d'inscription_equipe
    """
    return render_template('inscription_equipe.html',
                           title='Inscription Equipe',
                           competitions=inscriptionOuverteEquipe())

@app.route('/connexion_organisateur')
def connexion_organisateur():
    """ Page de connexion pour les organisateurs

    Returns:
        fonction: affiche la page de connexion_organisateur
    """
    return render_template('connexion_organisateur.html',
                           title='Connexion_organisateur')

##Fonctions de redirection vers les pages avec connexion

@app.route('/profil/<nbLicense>&<nbCompet>')
def profil(nbLicense,nbCompet):
    """ Page de profil de l'escrimeur

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page de profil
    """
    return render_template('profil.html',
                           title='Mon profil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                            nbLicense=int(nbLicense),
                            nbCompet=int(nbCompet),
                            informations=getProfil(int(nbLicense)),
                            stats=getStatistique(int(nbLicense)))

@app.route('/accueil/<nbLicense>&<nbCompet>')
def accueil(nbLicense,nbCompet):
    """ Page d'accueil pour une compétition

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page d'accueil de la compétition
    """
    return render_template('accueil.html',
                           title='Accueil',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                           nbCompet=int(nbCompet),
                           nbLicense=int(nbLicense),
                           nomCompet=getInfoCompetition(int(nbCompet))[0][1],
                           nombreCompet=len(getTournoisClosedParticiper(int(nbLicense))))

@app.route('/classement_national/<nbLicense>&<nbCompet>')
def classement_national(nbLicense,nbCompet):
    """ Page du classement national des escrimeurs

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page du classement national
    """
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                           nbCompet=int(nbCompet),
                           nbLicense=int(nbLicense))

@app.route('/archives/<nbLicense>&<nbCompet>')
def archives(nbLicense,nbCompet):
    """ Page des archives des compétitions

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page des archives
    """
    return render_template('archives.html',
                           title='Archives',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                           nbLicense=int(nbLicense),
                           nbCompet=int(nbCompet),
                           villes=getListeComiteReg(),
                           competitions=getListTournoisAllCLosed(),
                           competitionsParticiper=getTournoisClosedParticiper(int(nbLicense)))

@app.route('/options_competitions/<nbLicense>')
def options_competitions(nbLicense):
    """ Page des options des compétitions pour un organisateur

    Args:
        nbLicense (int): Numéro de licence de l'organisateur

    Returns:
        fonction: affiche la page des options des compétitions
    """
    return render_template('options_competitions.html',
                           title='Options_Compétitions',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           mesCompetitions=getCompetitionParOrga(nbLicense),
                           tournoisArchiver=getListIdCompetitionTournoisClosed(),
                           tournoisLancer=getListIdCompetitionTournoisLancer())

@app.route('/infoCompetition/<nbLicense>&<nbCompet>')
def infoCompetition(nbLicense,nbCompet):
    """ Page d'information d'une compétition

    Args:
        nbLicense (int): Numéro de licence de l'organisateur
        nbCompet (int): Numéro de compétition que l'on veut avoir des informations

    Returns:
        fonction: affiche la page d'information de la compétition
    """
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
    """ Page de création d'une compétition

    Args:
        nbLicense (int): Numéro de licence de l'organisateur

    Returns:
        fonction: affiche la page de création d'une compétition
    """
    return render_template('creation_competition.html',
                           title='Création_Compétition',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           nbLicense=int(nbLicense),
                           villes=getListeComiteReg())

@app.route('/resultats/<nbLicense>&<nbCompet>')
def resultats(nbLicense,nbCompet):
    """ Page des résultats d'une compétition
    la page est différente si l'escrimeur est un arbitre ou un participant ou un spectateur/organisateur

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page des résultats
    """
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
                            isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
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
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
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
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
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
                            isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
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
    """ Page des résultats d'une compétition en équipe
    la page est différente si l'escrimeur est un arbitre ou un participant/spectateur/organisateur

    Args:
        nbLicense (int): Numéro de licence de l'escrimeur
        nbCompet (int): Numéro de la compétition auquel l'escrimeur s'est connecté

    Returns:
        fonction: affiche la page des résultats en équipe
    """
    nbPartipant = getNbEquipe(int(nbCompet))
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
            return render_template('resultats_equipe.html',
                            title='Résultats Equipe',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=maFonctionPlusBelleQueLautreAvecPhase(int(nbCompet),getNbPhase(int(nbCompet))),
                            isArbitre=True,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=maFonctionPlusBelleQueLautre(int(nbCompet)),
                            lancer=lancer,
                            classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                            nbTotalPhase=nbTotalPhase,
                            classement=getClassementEquipFinal(nbCompet))
        else:
            return render_template('resultats_equipe.html',
                                title='Résultats Equipe',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=maFonctionPlusBelleQueLautre(int(nbCompet)),                                
                                lancer=lancer,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                nbTotalPhase=nbTotalPhase,
                            classement=getClassementEquipFinal(nbCompet))
    else:
        return render_template('resultats_equipe.html',
                            title='Résultats Equipe',
                            isOrganisateur=estOrganisateur(int(nbLicense)),
                            isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                            nbCompet=int(nbCompet),
                            nbLicense=int(nbLicense),
                            participants=[],
                            isArbitre=False,
                            nbPhase=getNbPhase(int(nbCompet)),
                            matchs=maFonctionPlusBelleQueLautre(int(nbCompet)),
                            lancer=lancer,
                            joueur=False,
                            nomCompet=getInfoCompet(int(nbCompet)),
                            arbitres=getNomArbitre(int(nbCompet)),
                            phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                            nbTotalPhase=nbTotalPhase,
                            classement=getClassementEquipFinal(nbCompet))

##Fonctions de vérification
## Penser a changer les render_template en redirect quand c'est possible !!!!

@app.route('/verifInscription')
def verifInscription():
    """ Fonction de vérification de l'inscription d'un escrimeur dans une compétition solo

    Returns:
        fonction: affiche la page d'inscription avec une popup en fonction de la vérification
    """
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
    """ Fonction de vérification de l'inscription d'un escrimeur dans une compétition en équipe

    Returns:
        fonction: affiche la page d'inscription_equipe avec une popup en fonction de la vérification
    """
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


@app.route('/verifConnexionEscrimeur')
def verifConnexionEscrimeur():
    """ Fonction de vérification de la connexion d'un escrimeur

    Returns:
        fonction: affiche la page de connexion_escrimeur avec une popup en fonction de la vérification
    """
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
    """ Fonction de vérification de la consultation des archives

    Returns:
        fonction: affiche la page résultat de la compétition souhaitée (equipe ou solo)
    """
    nbLicense = request.args.get("nbLicense")
    nbCompet = request.args.get("nbCompet")
    ancienNbCompet = request.args.get("ancienNbCompet")
    
    if isCompetitionEquipe(int(nbCompet)):
        nbPartipant = getNbEquipe(int(nbCompet))
    else:
        nbPartipant = getNbParticipant(int(nbCompet))
    nbTotalPhase = nbPartipant
    trouve = False
    i=0
    while not trouve:
        if nbPartipant <= 2**i:
            nbTotalPhase = i
            trouve = True
        i+=1
        
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    if isCompetitionEquipe(int(nbCompet)):
        return render_template('resultats_equipe.html',
                                title='Résultats Equipe',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=maFonctionPlusBelleQueLautre(int(nbCompet)),                                
                                lancer=True,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                ancienNbCompet=ancienNbCompet,
                                nbTotalPhase=nbTotalPhase,
                            classement=getClassementEquipFinal(nbCompet))
    else:
        return render_template('resultats.html',
                                title='Résultats',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
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
                                ancienNbCompet=ancienNbCompet,
                                nbTotalPhase=nbTotalPhase)

@app.route('/pageImprimerResultat')
def pageImprimerResultat():
    """ Page d'impression des résultats d'une compétition solo

    Returns:
        fonction: affiche la page d'impression des résultats solo
    """
    nbLicense = request.args.get("nbLicense")
    nbCompet = request.args.get("nbCompet")
    ancienNbCompet = request.args.get("ancienNbCompet")
    
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    return render_template('pageImprimerResultat.html',
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

@app.route('/pageImprimerResultatEquipe')
def pageImprimerResultatEquipe():
    """ Page d'impression des résultats d'une compétition en équipe

    Returns:
        foncrion: affiche la page d'impression des résultats en équipe
    """
    nbLicense = request.args.get("nbLicense")
    nbCompet = request.args.get("nbCompet")
    ancienNbCompet = request.args.get("ancienNbCompet")
    if isCompetitionEquipe(int(nbCompet)):
        nbPartipant = getNbEquipe(int(nbCompet))
    else:
        nbPartipant = getNbParticipant(int(nbCompet))
    nbTotalPhase = nbPartipant
    trouve = False
    i=0
    while not trouve:
        if nbPartipant <= 2**i:
            nbTotalPhase = i
            trouve = True
        i+=1
    listLicense=affichageGenererPhaseEliminations(int(nbCompet), getNbPhase(int(nbCompet)))
    licence=[]
    licence.append(listLicense[3])
    licence.append(listLicense[4])
    licence.append(listLicense[5])
    licence.append(listLicense[6])
    return render_template('pageImprimerResultatEquipe.html',
                                title='Résultats Equipe',
                                isOrganisateur=estOrganisateur(int(nbLicense)),
                                isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                                nbCompet=int(nbCompet),
                                nbLicense=int(nbLicense),
                                isArbitre=False,
                                nbPhase=getNbPhase(int(nbCompet)),
                                matchs=maFonctionPlusBelleQueLautre(int(nbCompet)),                                
                                lancer=True,
                                classements=classementFinale(int(nbCompet),getNbPhase(int(nbCompet))),
                                joueur=False,
                                nomCompet=getInfoCompet(int(nbCompet)),
                                arbitres=getNomArbitre(int(nbCompet)),
                                phaseFinie=phasesFinie(int(nbCompet),int(getNbPhase(int(nbCompet)))),
                                ancienNbCompet=ancienNbCompet,
                                nbTotalPhase=nbTotalPhase,
                                classement=getClassementEquipFinal(nbCompet))

@app.route('/traitement')
def traitement():
    """ Fonction de traitement de la connexion d'un organisateur

    Returns:
        fonction: redirect vers la page d'options_competitions si c'est un organisateur, sinon affiche la page de connexion_organisateur
    """
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
    """ Fonction de recherche des archives

    Returns:
        fonction: affiche la page des archives avec la recherche effectuée
    """
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    ville=request.args.get("ville")
    nbLicense=request.args.get("nbLicense")
    nbCompet=request.args.get("nbCompet")
    return render_template('archives.html',
                           title='Archives',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                           nbLicense=int(nbLicense),
                            nbCompet=int(nbCompet),
                           villes=getListeComiteReg(),
                           competitions=trieArchive(str(arme),str(sexe),str(categorie),str(ville)),
                           competitionsParticiper=getTournoisClosedParticiper(int(nbLicense)))

@app.route('/rechercheArchivesNC')
def rechercheArchivesNC():
    """ Fonction de recherche des archives pour un non connecté

    Returns:
        fonction: affiche la page des archives avec la recherche effectuée
    """
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
    """ Fonction de recherche du classement national

    Returns:
        fonction: affiche la page du classement national avec la recherche effectuée
    """
    arme=request.args.get("arme")
    sexe=request.args.get("sexe")
    categorie=request.args.get("categorie")
    nbLicense=request.args.get("nbLicense")
    nbCompet=request.args.get("nbCompet")
    return render_template('classement_national.html',
                           title='Classement_National',
                           isOrganisateur=estOrganisateur(int(nbLicense)),
                           isCompetitionEquipe=isCompetitionEquipe(int(nbCompet)),
                           nbLicense=int(nbLicense),
                           nbCompet=int(nbCompet),
                           classement=getClassementNationnal(arme,sexe,categorie))

@app.route('/validationConnexion')
def validationConnexion():
    """ Fonction de validation de la connexion d'un escrimeur

    Returns:
        fonction: redirect vers la page d'accueil d'une compétition
    """
    nbCompet=request.args.get("compet")
    nbLicense=request.args.get("nbLicense")
    return redirect('accueil/'+str(nbLicense)+'&'+str(nbCompet))


@app.route('/creationCompetition')
def creationCompetition():
    """ Fonction de création d'une compétition

    Returns:
        fonction: redirect vers la page d'options_competitions avec la compétition créée
    """
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
    """ Fonction de lancement d'une compétition

    Returns:
        fonction: redirect vers la page d'options_competitions avec la compétition lancée
    """
    lancerCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))

@app.route('/boutonArchiver')
def boutonArchiver():
    """ Fonction d'archivage d'une compétition

    Returns:
        fonction: redirect vers la page d'options_competitions avec la compétition archivée
    """
    archiverCompetition(int(request.args.get("nbCompet")))
    return redirect('options_competitions/'+str(request.args.get("nbLicense")))

@app.route('/update_data', methods=['POST'])
def update_data():
    """ Fonction de mise à jour des données d'une compétition

    Returns:
        fonction: redirect vers la page resultat avec la compétition mise à jour
    """
    data = request.form.get('data')
    nbLicenceTireur = request.form.get('nbLicenceTireur')
    nbLicenceTireurAdverse = request.form.get('nbLicenceTireurAdverse')
    numCompetition = request.form.get('numCompetition')
    nbPhase = request.form.get('nbPhase')
    setToucherDonneTireur(int(nbLicenceTireur), int(nbLicenceTireurAdverse), int(data), int(numCompetition), int(nbPhase))
    return redirect('resultats/'+str(nbLicenceTireur)+'&'+str(numCompetition))


@app.route('/genererEliminations', methods=['POST'])
def genererEliminations():
    """ Fonction de génération des phases d'éliminations

    Returns:
        fonction: redirect vers la page resultat avec la compétition mise à jour
    """
    nbCompet = int(request.form.get('nbCompet'))
    nbPhase = int(request.form.get('nbPhase'))
    nbLicense = int(request.form.get('nbLicense'))
    # print('\033[93m' + str(nbCompet) + '\033[0m')
    # print('\033[93m' + str(nbPhase) + '\033[0m')
    genererPhaseEliminations(int(nbCompet), int(nbPhase)+1)
    return redirect('resultats/'+str(nbLicense)+'&'+str(nbCompet))

@app.route('/ajouterPoints', methods=['POST'])
def ajouterPoints():
    """ Fonction d'ajout de points a une équipe

    Returns:
        fonction:  redirect vers la page resultat_equipe avec la compétition mise à jour
    """
    nbLicence=request.form.get('nbLicense')
    nbCompet = int(request.form.get('numCompet'))
    nbPhase = getNbPhase(nbCompet)
    nomPoint = request.form.get('nomPoint')
    nomLose = request.form.get('nomLose')
    addPointMatchEquipe(nbCompet, nbPhase, nomPoint, nomLose)
    return redirect('resultats_equipe/'+str(nbLicence)+'&'+str(nbCompet))

@app.route('/enleverPoints', methods=['POST'])
def enleverPoints():
    """ Fonction de retrait de points a une équipe

    Returns:
        fonction: redirect vers la page resultat_equipe avec la compétition mise à jour
    """
    nbLicence=request.form.get('nbLicense')
    nbCompet = int(request.form.get('numCompet'))
    nbPhase = getNbPhase(nbCompet)
    nomPoint = request.form.get('nomPoint')
    nomLose = request.form.get('nomLose')
    subPointMatchEquipe(nbCompet, nbPhase, nomPoint, nomLose)
    return redirect('resultats_equipe/'+str(nbLicence)+'&'+str(nbCompet))
    


@app.route('/genererPhaseEquipe', methods=['POST'])
def genererPhaseEquipe():
    """ Fonction de génération des phases d'éliminations en équipe

    Returns:
        fonction: redirect vers la page resultat_equipe avec la compétition mise à jour
    """
    nbCompet = int(request.form.get('nbCompet'))
    nblicense = int(request.form.get('nbLicense'))
    listeNomVictoire=request.form.getlist('nomVictoire')
    generePhaseSuivanteEquipe(int(nbCompet), str(listeNomVictoire))
    return redirect('resultats_equipe/'+str(nblicense)+'&'+str(nbCompet))

