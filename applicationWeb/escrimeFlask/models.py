import csv



# pip install Flask-MySQLdb
#sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config


import os.path

# -*- coding: utf-8 -*-
import mysql.connector

#connexion au base de données
db = mysql.connector.connect(
  host = "localhost",
  user = "koko",
  password = "koko",
  database = "Escrime"
)
#Blabla2147
#créer un curseur de base de données pour effectuer des opérations SQL
cursor = db.cursor()

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

def getIdLieuByNom(nomLieu): 
    try :
        requete = "select idLieu from LIEU where comiteReg = '" + str(nomLieu) +"' ;"
        cursor.execute(requete)
        return cursor.fetchall()[0][0]
    except Exception : 
        return None

def setNewLieuByNom(nomLieu): 
    requete = "insert into LIEU(adresse,region,departement,comiteReg) values('"+ str(nomLieu) +"','"+ str(nomLieu) +"','" + str(nomLieu) + "', '" + str(nomLieu) + "' )"
    cursor.execute(requete)
    db.commit()

def getIdCategorieByNom(nomCat): 
    requete = "select idCategorie from CATEGORIE where intituleCategorie = '" + str(nomCat) +"' ;"
    cursor.execute(requete)
    return cursor.fetchall()[0][0]

def getIdSexeByNom(nomSexe): 
    requete = "select idSexe from SEXE where intituleSexe = '" + str(nomSexe) +"' ;"
    cursor.execute(requete)
    return cursor.fetchall()[0][0]


def getIdArmeByNom(nomArme): 
    requete = "select idArme from ARME where typeArme = '" + str(nomArme) +"' ;"
    cursor.execute(requete)
    return cursor.fetchall()[0][0]

def getIdClubByNom(nomClub): 
    requete = "select idClub from CLUB where nomClub = '" + str(nomClub) +"' ;"
    cursor.execute(requete)
    return cursor.fetchall()[0][0]



def getIdSexeByIdCompetition(idCompetition : int) -> int:
  requete = "select idSexeCompetition from COMPETITION where idCompetition = " + str(idCompetition) + ";"
  cursor.execute(requete)
  return cursor.fetchall()

def getIdMaxCompetition() -> int :
    requete = "select MAX(idCompetition) from COMPETITION;"
    cursor.execute(requete)
    return cursor.fetchall()[0][0]

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

def insertTireurDansCompetition(nom : str, prenom : str,numeroLicence : int , dateNaissanceTireur : str, nomCLub :str, idCompetition: int, ToA : str) -> bool:
    try :
        if estDansBDNational(numeroLicence) :
          try :
            #Verifié si les info données correspondent aux valeurs de la BD national
            infoTireur = getInfoFromBDNational(numeroLicence)
            if infoTireur != False : # si le numéro de licence est dans la BD national
              infs = infoTireur[1] # On prend la infos de la personne qui veut s'inscrire 
              if infs[0].lower() == nom.lower() and infs[1].lower() == prenom.lower() and corrigerDate(infs[2]) == dateNaissanceTireur and infs[6].lower() == nomCLub.lower() : # On regarde si les infos passé correspondent au csv
                # Il manque de vérifié le genre de la compète et idSexe + si arbitre ou tireur est passé en paremètre
                if ToA.upper() == 'TIREUR' : 
                  insertTireurDansBD(numeroLicence)
                  if getIdSexeByIdCompetition(idCompetition) == getIdSexeByNumLicence(numeroLicence) :
                    requete5 = "insert into TIREUR_DANS_COMPETITIONS (numeroLicenceTireur,idCompetition) values(%s,%s);"
                    cursor.execute(requete5, (numeroLicence,idCompetition))
                    db.commit()
                    return True  
                  else : 
                    return False #pas le bon idSexe
                else : 
                  insertArbitreDansBD(numeroLicence)
                  requete5 = "insert into ARBITRE_DANS_COMPETITIONS(numeroLicenceArbitre,idCompetition) values(%s,%s);"
                  cursor.execute(requete5, (numeroLicence,idCompetition))
                  db.commit()
                  return True  
            return False # au moins une des autre close qui vas pas 
          except Exception as mysql_error:
            print(mysql_error)
            return False
        else : 
          return False
    except Exception as mysql_error:
      print(mysql_error)
      return False


def insertTireurDansBD(numeroLicence : int) : 
   if estDansBDNational(numeroLicence) : 
      try :
        infoTireurGlobal = getInfoFromBDNational(numeroLicence)
        # = ['PETIT', 'Stéphane', '02/09/1963', '138932', 'FRANCE', 'ILE DE FRANCE Ouest', 'NEUILLY ESCR', '1687', '149']
        infoTireur = infoTireurGlobal[1]
        idSexe = infoTireurGlobal[0]
        if "Dames" in str(idSexe) : 
           idSexe = 2
        else : 
           idSexe = 1
        requete1 = "insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur,dateNaissanceTireur,nationTireur,comiteRegionalTireur) values(%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(requete1, (infoTireur[0],infoTireur[1],numeroLicence,infoTireur[7],idSexe,corrigerDate(infoTireur[2]),infoTireur[4],infoTireur[5]))
        db.commit()
        return True
      except Exception as mysql_error:
        print(mysql_error)
        return False
      

def insertArbitreDansBD(numeroLicence : int) : 
   if estDansBDNational(numeroLicence) : 
      try :
        infoTireurGlobal = getInfoFromBDNational(numeroLicence)
        # = ['PETIT', 'Stéphane', '02/09/1963', '138932', 'FRANCE', 'ILE DE FRANCE Ouest', 'NEUILLY ESCR', '1687', '149']
        infoTireur = infoTireurGlobal[1]
        idSexe = infoTireurGlobal[0]
        if "Dames" in str(idSexe) : 
           idSexe = 2
        else : 
           idSexe = 1
        requete1 = "insert into ARBITRE(nomArbitre,prenomArbitre,numeroLicenceArbitre) values(%s,%s,%s);"
        cursor.execute(requete1, (infoTireur[0],infoTireur[1],numeroLicence))
        db.commit()
        return True
      except Exception as mysql_error:
        print(mysql_error)
        return False
      

def corrigerDate(date :str) -> str : 
   newDate = date[6] + date[7] + date[8] + date[9] + "-" + date[3] + date[4] + "-" + date[0] + date[1]
   return newDate

def crypterDate(date :str) -> str : 
   newDate = date[8] + date[9] + "/" +  date[5] + date[6] + "/" + date[0] + date[1] + date[2] + date[3]
   return newDate

def getInfoFromBDNational(numeroLicence : int) -> list :
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
    for cat in infoFichier :
       if str(numeroLicence) == cat[3] :
          # cat =  nom[0]  prenom[1]  dateNaissance[2]  licence[3]  nation[4]  comiteReg[5]  CLUB[6]  point[7]  classement[8] 
          return [f,cat]
  return False


def getListeComiteReg():
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  listeComiteReg = []
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
    for comite in infoFichier :
      if comite[5] not in listeComiteReg :
        listeComiteReg.append(comite[5])
  return listeComiteReg


def estDansBDNational(numeroLicence : int) -> bool:
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask//csvEscrimeur/" + f)
    for cat in infoFichier :
       if str(numeroLicence) == cat[3] :
          return True
  return False 


def concourtInscritLicenceTireur(numeroLicence : int) -> list:
  requete1 = "select * from TIREUR_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceTireur = " + str(numeroLicence) + ";"
  cursor.execute(requete1)
  info = cursor.fetchall()
  return infoCompetitionOuverte(info)

def concourtNonFinitInscritTireur(licenceTireur) : 
  requete1 = "select * from TIREUR_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceTireur = " + str(licenceTireur) + ";"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                  from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                  where estFinie = False and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
    cursor.execute(requete2) 
    ligneAj = cursor.fetchall()
    if ligneAj != [] :
      res.append(ligneAj)
  return res

def concourtNonFinitInscritArbitre(licenceArbitre) : 
  requete1 = "select * from ARBITRE_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceArbitre = " + str(licenceArbitre) + ";"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                  from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                  where estFinie = False and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
    cursor.execute(requete2) 
    ligneAj = cursor.fetchall()
    if ligneAj != [] :
      res.append(ligneAj)
  return res


def concourtInscritLicenceArbitre(numeroLicence : int) -> list:
  requete1 = "select * from ARBITRE_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceArbitre = " + str(numeroLicence) + ";"
  cursor.execute(requete1)
  info = cursor.fetchall()
  return infoCompetitionOuverte(info)
  # return sous la forme : nomCompetition intituleCompet typeArme intituleSexe intituleCategorie departement
  

def classementFile(filename :str) -> list:
    "nom prenom date_naissance adherent nation comite_regional club points rang"
    res = []
    with open(filename, 'r',encoding='Latin-1') as file :
      next(file)
      for ligne in file:
        ligne = ligne.split(";")
        ligne[8] = ligne[8].replace("\n","")
        res.append(ligne)
      file.close()
    return res

def getClassementNationnal(arme,sexe,categorie) : 
  return classementFile("./escrimeFlask/csvEscrimeur/classement_" + arme + "_" + sexe + "_" + categorie +".csv")


def inscriptionOuverte() -> list:
  requete1 = "select * from COMPETITION where datediff(dateDebutCompetiton, CURDATE()) > 14 and estFinie = False;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                  from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                  where datediff(dateDebutCompetiton ,CURDATE()) > 14 and estFinie = False and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +";"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res


def getOrganisateurClub():
  requete1 = "select * from ORGANISATEURDANSCLUB natural join CLUB ;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = dict()
  for i in range(len(info)):
    res[info[i][1]] = info[i][2]
  return res


def getIdSexeByNumLicence(numeroLicence : int) -> int:
  requete = "select idSexeTireur from TIREUR where numeroLicenceTireur = " + str(numeroLicence) + ";"
  cursor.execute(requete)
  return cursor.fetchall()

def estOrganisateur(numeroLicence : int) :
  requete = "select nomOrganisateur from ORGANISATEUR where licenseOrganisateur = " + str(numeroLicence) + ";"
  cursor.execute(requete)
  return cursor.fetchall() != []


def infoCompetitionOuverte(info):
  res = []
  for i in range(len(info)):
      requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                    from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                    where datediff(dateDebutCompetiton ,CURDATE()) > 14 and estFinie = False and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
      cursor.execute(requete2) 
      res.append(cursor.fetchall())
  return res

def getInfoCompetition(idCompetiton):
  requete = "select * from COMPETITION where idCompetition = " + str(idCompetiton) + ";"
  cursor.execute(requete)
  return cursor.fetchall() 

def infoCompetitionFinie(info):
  res = []
  for i in range(len(info)):
    
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                 from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                where estFinie = True and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +"  order by dateDebutCompetiton DESC;"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res

def infoCompetitionOuverte(info):
  res = []
  for i in range(len(info)):
    
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                 from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                where estFinie = False and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +"  order by dateDebutCompetiton DESC;"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res

def getListTournoisAllCLosed():
  requete1 = "select * from COMPETITION where estFinie = True order by dateDebutCompetiton DESC;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  return infoCompetitionFinie(info)

def getListIdCompetitionTournoisClosed():
  listeIdCompetition = []
  liste = getListTournoisAllCLosed()
  for i in range(len(liste))  : 
    listeIdCompetition.append(liste[i][0][5])
  return listeIdCompetition

def getTournoisLancer():
  requete1 = "select * from COMPETITION where estFinie = False and datediff(dateDebutCompetiton,CURDATE()) < 1 order by dateDebutCompetiton DESC;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  return infoCompetitionOuverte(info)

def getListIdCompetitionTournoisLancer():
  listeIdCompetition = []
  liste = getTournoisLancer()
  for i in range(len(liste)): 
    listeIdCompetition.append(liste[i][0][5])
  return listeIdCompetition

def getTournoisClosedParticiper(numeroLicence):
  requete1 = "select * from TIREUR_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceTireur = " + str(numeroLicence) + " and estFinie = True  order by dateDebutCompetiton DESC;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                 from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                where estFinie = True and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +"  order by dateDebutCompetiton DESC ;"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res

def getProfil(numLicence): 
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  profil = []
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
    for comite in infoFichier :
      if int(comite[3]) == numLicence :
        profil.append(comite[0:7])
  return profil

def trieArchive(arme, sexe, categorie, region):
  liste = getListTournoisAllCLosed()
  liste2 = []
  for comp  in liste : 
    cpt = 0
    if arme != "none" : 
      if comp[0][1] == arme : cpt += 1
    else : cpt += 1

    if sexe != "none" :
      if comp[0][2] == sexe : cpt += 1
    else : cpt += 1

    if categorie != "none" :
      if comp[0][3] == categorie : cpt += 1
    else : cpt += 1

    if region != "none" :
      if comp[0][4] == region : cpt += 1 
    else : cpt += 1

    if cpt == 4 : liste2.append(comp)

  return liste2


def getStatistique(numLicence):
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  stats = []
  for f in fichiers :
    if "Epée" in f  :
      infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
      for ligne in infoFichier :
        if int(ligne[3]) == numLicence :
          stats.append(("Épée",ligne[7],ligne[8]))
    if "Sabre" in f  :
      infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
      for ligne in infoFichier :
        if int(ligne[3]) == numLicence :
          stats.append(("Sabre",ligne[7],ligne[8]))
    if "Fleuret" in f  :
      infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
      for ligne in infoFichier :
        if int(ligne[3]) == numLicence :
          stats.append(("Fleuret",ligne[7],ligne[8]))
  return stats

def getCompetitionParOrga(numLicence): 
  requete = "select * from ORGANISATEURCOMPETITION natural join COMPETITION  where licenseOrganisateur = " + numLicence + " order by dateDebutCompetiton DESC;"
  cursor.execute(requete)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                 from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                where  idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +" order by dateDebutCompetiton DESC;"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res

def createCompetition(nomCompete, lieu, categorie, sexe, arme, coef, date, licenceOrga ) : 
  if getIdLieuByNom(lieu) is None : setNewLieuByNom(lieu)
  requete1 = """insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) 
                values ('""" + str(nomCompete) + "'," + str((date)[0:4]) + "," + "False" + "," + str(coef) + ",'" + str((date)) + "'," + str(getIdLieuByNom(lieu)) + "," + str(getIdCategorieByNom(categorie))+ "," + str(getIdSexeByNom(sexe)) +"," + str(getIdArmeByNom(arme)) + ");"""
  cursor.execute(requete1)
  db.commit()
  idComp = int(getIdMaxCompetition())
  requete2 = "insert into ORGANISATEURCOMPETITION(idCompetition, licenseOrganisateur) values( " + str(idComp) + "," + str(licenceOrga) + ");"
  cursor.execute(requete2)
  db.commit()

def archiverCompetition(idCompetition): 
  requete = "update COMPETITION set estFinie = True where idCompetition = " + str(idCompetition) + ";"
  cursor.execute(requete)
  db.commit()

def lancerCompetition(idCompetition): 
  requete = "update COMPETITION set dateDebutCompetiton = CURDATE() where idCompetition = " + str(idCompetition) + ";"
  cursor.execute(requete)
  db.commit()

def competitionEstFinie(idCompetition): 
  requete = "select estFinie from COMPETITION where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  return cursor.fetchall()

def competitionEstLancer(idCompetition): 
  requete = "select datediff(dateDebutCompetiton,CURDATE()) from COMPETITION where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  return cursor.fetchall() == 0

def fichiersDossier(path : str) :
  files = os.listdir(path)
  listeChemin = []
  for name in files:
    listeChemin.append(name)
  return listeChemin

########################################################################
########################################################################
##################### Lancement Competition ############################
########################################################################
########################################################################

def getNbTireur(idCompetition): 
  requete = "select * from COMPETITION natural join TIREUR_DANS_COMPETITIONS where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  return len(cursor.fetchall())
  
def getNbArbitre(idCompetition):
  requete = "select * from COMPETITION natural join ARBITRE_DANS_COMPETITIONS where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  return len(cursor.fetchall())

def getInfoTireurs(idCompetition): 
  requete = "select idCompetition, numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_COMPETITIONS natural join TIREUR where idCompetition = "+str(idCompetition)+" order by classement DESC;"
  cursor.execute(requete)
  return cursor.fetchall()

def getInfoArbitres(idCompetition): 
  requete = "select idCompetition, numeroLicenceArbitre from COMPETITION natural join ARBITRE_DANS_COMPETITIONS where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  return cursor.fetchall()

def getIdPouleTireur(numLicenceTireur, idCompetition = 1) : 
  requete = "select idPoule from POULE natural join TIREUR_DANS_POULE where numeroLicenceTireur = " + str(numLicenceTireur) + "  and idCompetition = " +str(idCompetition) + ";"
  cursor.execute(requete)
  return cursor.fetchall()[0][0]

def getIdPouleArbitre(numLicenceArbitre, idCompetition) :
  requete = "select idPoule from POULE natural join ARBITRE_POULE where numeroLicenceArbitre = " + str(numLicenceArbitre) + " and idCompetition = " +str(idCompetition) + " ;"
  cursor.execute(requete)
  return cursor.fetchall()[0][0]

def getNomByLicence(licence) : 
  requete = "select nomTireur, prenomTireur from TIREUR  where numeroLicenceTireur = " + str(licence) + ";"
  cursor.execute(requete)
  res = cursor.fetchall()[0]
  return res[0], res[1]

def getNomClubByLicence(licence) : 
  requete = "select nomClub from CLUB natural join TIREUR_DANS_CLUB where numeroLicenceTireur = " + str(licence) + ";"
  cursor.execute(requete)
  res = cursor.fetchall()[0]
  return res[0]


def getListeidPouleCompetition(idCompetition) : 
  requete = "select idPoule from POULE  where idCompetition = " + str(idCompetition) + ";"
  cursor.execute(requete)
  res = cursor.fetchall()
  liste = []
  for elem in res :
    liste.append(elem[0])
  return liste

# (numLicence, num) : (nom,prenom,club,[(num,toucheDonnee,toucheRecu)], toucheDonnéeTotal, toucheRecuTotal,victoire,placeClassement)
def setToucherDonneTireur(licenceTireur1, licenceTireur2, toucheDTireur, idCompetition, nbPhase) :
  idPoule = getIdPouleTireur(licenceTireur1, idCompetition)
  requete = "select licenceTireur1 from MATCHPOULE where licenceTireur1 = " + str(licenceTireur1) + " and licenceTireur2 = " + str(licenceTireur2) + " and idPoule = " + str(idPoule) + ";"
  cursor.execute(requete)
  l1 = cursor.fetchall()
  print(l1)
  if l1 != [] :
    requete = "update MATCHPOULE set toucheDTireur1 = " + str(toucheDTireur) + " where licenceTireur1 = " + str(licenceTireur1) + " and licenceTireur2 = " + str(licenceTireur2) + " and idPoule = " + str(idPoule) + " and nbPhases = "+ str(nbPhase) +";"
  else:
    requete = "update MATCHPOULE set toucheDTireur2 = " + str(toucheDTireur) + " where licenceTireur1 = " + str(licenceTireur2) + " and licenceTireur2 = " + str(licenceTireur1) + " and idPoule = " + str(idPoule) + " and nbPhases = "+ str(nbPhase) +";"      
  cursor.execute(requete)
  db.commit()

# (numLicence, num) : (nom,prenom,club,[(num,toucheDonnee,toucheRecu)], toucheDonnéeTotal, toucheRecuTotal)
#(25151,1) :  nathan, escriClub, [(2,5),(3,2)]
def InfosPouleNumLicence(idCompetition, numLicenceTireur) : 
  listeNumLicencePoule = []
  idPoule = getIdPouleTireur(numLicenceTireur, idCompetition)
  requete = "select distinct numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_POULE where idCompetition = "+ str(idCompetition) +" and idPoule = " + str(idPoule) + ";"
  cursor.execute(requete)
  listeNumLicencePoule = cursor.fetchall()
  for t in range(len(listeNumLicencePoule)) : 
    listeNumLicencePoule[t] = listeNumLicencePoule[t][0]
  # "select licenceTireur1,licenceTireur2, toucheDTireur1  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + idCompetition + "and numeroLicenceTireur = " + numLicenceTireur + " and licenceTireur1 = " + numLicenceTireur+";"
 
 
  dico = dict()
  for numLicence in range(len(listeNumLicencePoule)) : 
    Lo = listeNumLicencePoule[numLicence]
    requete = "select distinct licenceTireur1,licenceTireur2, toucheDTireur1, toucheDTireur2  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + str(idCompetition) + " and ( numeroLicenceTireur = " + str(Lo) + " and licenceTireur1 = " + str(Lo)+") or ( licenceTireur2 = " + str(Lo)+") ;"
    cursor.execute(requete)
    res = cursor.fetchall()
    key = (Lo,listeNumLicencePoule.index(Lo)+1)
    nom, prenom = getNomByLicence(Lo)
    club = getNomClubByLicence(Lo)
    listeMatch = []
    for j in range(len(res)) :
      if res[j][0] == Lo : 
        listeMatch.append((res[j][1],res[j][2],res[j][3]))
      else : 
        listeMatch.append((res[j][0],res[j][3],res[j][2]))
    listeMatch.reverse()
    listeMatch.insert(listeNumLicencePoule.index(Lo),(Lo,-2,-2))
    nbTotalTouchesDonnees = 0
    nbTotalTouchesRecues = 0
    victoire = 0
    for participant in listeMatch:
      if participant[1] != -1 and participant[2] != -1 :
        if participant[1] != -2 and participant[2] != -2 :
          nbTotalTouchesDonnees += participant[1]
          nbTotalTouchesRecues += participant[2]

      if participant[1] == 5:
        victoire+=1
    dico[key] = (nom,prenom,club,listeMatch,nbTotalTouchesDonnees,nbTotalTouchesRecues,victoire,0)
  # print(dico)
  dico = classementPoule(dico)
  return dico

def InfosPouleNumLicenceArbitre(idCompetition, numLicenceArbitre) : 
  listeNumLicencePoule = []
  idPoule = getIdPouleArbitre(numLicenceArbitre, idCompetition)
  requete = "select distinct numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_POULE where idCompetition = "+ str(idCompetition) +" and idPoule = " + str(idPoule) + ";"
  cursor.execute(requete)
  listeNumLicencePoule = cursor.fetchall()
  for t in range(len(listeNumLicencePoule)) : 
    listeNumLicencePoule[t] = listeNumLicencePoule[t][0]
  # "select licenceTireur1,licenceTireur2, toucheDTireur1  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + idCompetition + "and numeroLicenceTireur = " + numLicenceTireur + " and licenceTireur1 = " + numLicenceTireur+";"
  dico = dict()
  for numLicence in range(len(listeNumLicencePoule)) : 
    Lo = listeNumLicencePoule[numLicence]
    requete = "select distinct licenceTireur1,licenceTireur2, toucheDTireur1, toucheDTireur2  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + str(idCompetition) + " and ( numeroLicenceTireur = " + str(Lo) + " and licenceTireur1 = " + str(Lo)+") or ( licenceTireur2 = " + str(Lo)+") ;"
    cursor.execute(requete)
    res = cursor.fetchall()
    key = (Lo,listeNumLicencePoule.index(Lo)+1)
    nom, prenom = getNomByLicence(Lo)
    club = getNomClubByLicence(Lo)
    listeMatch = []
    for j in range(len(res)) :
      if res[j][0] == Lo : 
        listeMatch.append((res[j][1],res[j][2],res[j][3]))
      else : 
        listeMatch.append((res[j][0],res[j][3],res[j][2]))
    listeMatch.reverse()
    listeMatch.insert(listeNumLicencePoule.index(Lo),(Lo,-2,-2))
    nbTotalTouchesDonnees = 0
    nbTotalTouchesRecues = 0
    victoire = 0
    for participant in listeMatch:
      if participant[1] != -1 and participant[2] != -1 :
        if participant[1] != -2 and participant[2] != -2 :
          nbTotalTouchesDonnees += participant[1]
          nbTotalTouchesRecues += participant[2]

      if participant[1] == 5:
        victoire+=1

    

    dico[key] = (nom,prenom,club,listeMatch,nbTotalTouchesDonnees,nbTotalTouchesRecues,victoire,0)
  # print(dico)
  dico = classementPoule(dico)
  return dico

def classementPoule(dico):
  #trier du 1 au dernier en fonction du nombre de victoire
  #si egalité, on regarde la différence de toucheDonnéeTotale - toucheRecuTotale

  #dico = (numLicence, num) : (nom,prenom,club,[(num,toucheDonnee,toucheRecu)], toucheDonnéeTotal, toucheRecuTotal)
  
  liste = []
  for key in dico.keys():
    liste.append(key)
  liste.sort(key=lambda x: (dico[x][6],dico[x][4]-dico[x][5]),reverse=True)
  print(liste)
  for i in range(len(liste)):
    dico[liste[i]] = (dico[liste[i]][0],dico[liste[i]][1],dico[liste[i]][2],dico[liste[i]][3],dico[liste[i]][4],dico[liste[i]][5],dico[liste[i]][6],i+1)
  return dico


def calculer_nombre_poules(liste_choix_part_poule, nb_part, nb_arbitre):

  listeNbPoule = []
  
  for choix in liste_choix_part_poule:
    ind = 0
    nbPoule = 0
    nbP = nb_part
    while nbP >= choix : 
      nbP -= choix
      nbPoule += 1
    if nbP > 0 : 
      nbPoule += 1
    listeNbPoule.append([choix,nbPoule,nbP])
  
  listeRetien = []

  if nb_arbitre == 0 : nb_arbitre = 1

  for elem in listeNbPoule : 
    if elem[1] % nb_arbitre == 0 and elem[0] != 5 : 
      listeRetien.append(elem)
    elif elem[1]-1 % nb_arbitre == 0 and elem[0] == 5:
      listeRetien.append(elem)

  choixR = -1
  if len(listeRetien) > 0 :
    
    for l in listeRetien :
      if choixR == -1 or l[2] > choixR[2] :
        choixR = l
    return choixR[0],choixR[1],choixR[2]
  else : 
    for elem in listeNbPoule :
      if elem[2] == 0 : 
        return elem
    return listeNbPoule[2]


def createPoule(idCompetition,nbPoule) : 
  for i in range(1,nbPoule+1):
    req = "insert into POULE(nomPoule, numeroPiste, idCompetition) value(  \" Poule"+str(i)+" \", 8," +str(idCompetition)+" );"
    cursor.execute(req)
    db.commit()


def insTireurDansPoule(infosTireur, idCompetition) : 
  nbTireur = len(infosTireur)
  listeIdPoule = getListeidPouleCompetition(idCompetition)
  minIdPoule = min(listeIdPoule)
  ind = 0 #ind  idPoule
  inc = 1 
  i = 0  # ind infoTireur
  while nbTireur > 0 : 
    nbTireur -= 1
    req = "insert into TIREUR_DANS_POULE(numeroLicenceTireur,idPoule) value ( "+str(infosTireur[i][1])+" ," +str(listeIdPoule[ind])+" );"
    i += 1
    try : 
      cursor.execute(req)
      db.commit()
    except Exception : 
      pass
    ind += inc 
    if ind >= len(listeIdPoule) : 
      ind -= 2  
      inc = 1
    elif ind == -1 : 
      inc = -1

def insArbitreDansPoule(infosArbitre, idCompetition) : 
  nbArbitre = len(infosArbitre)
  listeIdPoule = getListeidPouleCompetition(idCompetition)
  nbPoule = len(listeIdPoule)
  ind = 0 #ind  idPoule
  i = 0  # ind infoTireur
  while nbPoule > 0 : 
    nbPoule -= 1 
    print(infosArbitre,i,nbArbitre,listeIdPoule,ind)
    req = "insert into ARBITRE_POULE(numeroLicenceArbitre,idPoule) value ( "+str(infosArbitre[i][1])+" ," +str(listeIdPoule[ind])+" );"
    try : 
      cursor.execute(req)
      db.commit()
    except Exception : 
      pass
    i += 1
    ind += 1
    if i >= nbArbitre : i = 0
    if ind >= len(listeIdPoule) : ind = 0 

def genererMatchPouleIdCompetition(idCompetition) : 
  listeIdPoule = getListeidPouleCompetition(idCompetition)
  for idPoule in listeIdPoule : 
    
    requete = "select distinct numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_POULE where idCompetition = "+ str(idCompetition) +" and idPoule = " + str(idPoule) + ";"
    cursor.execute(requete)
    l = cursor.fetchall()
    listeNumLicence = []
    for numL in range(len(l)) : 
      listeNumLicence.append(l[numL][0])

    indDepart = 1 
    for i in range(len(listeNumLicence)-1): 
      for j in range(indDepart,len(listeNumLicence)): 
        listeNumLicence[i], listeNumLicence[j] 
        nomMatch = "Match: " + str(getNomByLicence(listeNumLicence[i])[0])+ "-" + str(getNomByLicence(listeNumLicence[j])[0])
    
        requete = "insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule) value(\" " + nomMatch +" \","+ str(listeNumLicence[i]) + " , "+ str(listeNumLicence[j])+",1, "+str(idPoule)+" );" 
        cursor.execute(requete)
        db.commit()

      indDepart += 1 




def lancerCompetition(idCompetition): 

  nbTireur,nbArbitre = getNbTireur(idCompetition), getNbArbitre(idCompetition)
  #if nbTireur < 5 or nbArbitre == 0 : return None
  infosTireur, infosArbitre = getInfoTireurs(idCompetition), getInfoArbitres(idCompetition)


  # 1) gener nbPoule en fonction nbTIreur et Arbitre
  listeChoixPartPoule, listePoules = [5,6,7,8,9], []
  choixTPP, nbPoule, resteT   = calculer_nombre_poules(listeChoixPartPoule, nbTireur, nbArbitre)
# pour le moment les tireurs ne sont pas mit dabs les poules c'est juste des testes pour voir si le model marche
  for i in range(nbPoule - 1 if choixTPP == 5 and resteT > 0 else nbPoule):
    listePoules.append([])

  
  ind = 0
  while nbTireur > 0 : 
    nbTireur -= 1 
    listePoules[ind].append(nbTireur) 
    ind += 1
    if ind >= len(listePoules): ind = 0


  createPoule(idCompetition,len(listePoules))
  insTireurDansPoule(infosTireur, idCompetition)
  insArbitreDansPoule(infosArbitre, idCompetition)
  genererMatchPouleIdCompetition(idCompetition)

  # 2) INSERT poule 
  # 3) insertBD TIREURDANSPOULES
  # 4)insertBD ArbitreDANSPOULES
  # 5) gener matchPoule
  # 6) les insert


if __name__ == "__main__":
    # print(getNomByLicence(315486))
    # print(InfosPouleNumLicence(1,315486))
    # print(getListeidPouleCompetition(1))

    print(getIdPouleTireur(315486))
    #print(lancerCompetition(1)) # Pour creer une competition pour les tests

    # print(genererMatchPouleIdCompetition(1))
    # print(lancerCompetition(1))
    # setToucherDonneTireur(213138, 315486, 15)
    # print(lancerCompetition(1))

    #print(inscriptionOuverte())
    
    # print(concourtInscritLicence(521531))
    # print(getOrganisateurClub())
    # print(getProfil(315486))
    # print(estDansBDNational(521531))
    # print(getInfoFromBDNational(138932))
    # print(insertTireurDansCompetition('CONY', 'Philippe' ,13659, '1961-07-06', 'NEUVY NA', 2,'tireur'))   # nom , prenom ,numeroLicence  , dateNaissanceTireur , nomCLub , idCompetition
    # print(estDansBDNational(13659))
    # print(concourtInscritLicenceTireur(13659))

    # print(concourtInscritLicenceArbitre(654123))
    # print(estOrganisateur(241354))
    # print(getListeComiteReg())
    # print(getListTournoisAllCLosed())
    # print(getTournoisClosedParticiper(151229))
    # print(concourtInscritLicenceTireur(151229))
    #print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(getCompetitionParOrga(254612))
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(getProfil(151229))
    # print(getCompetitionParOrga(254612))
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(getProfil(123261))

    # print(getCompetitionParOrga(254612))
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    #print(getProfil(151229))
    # print(concourtInscritLicenceTireur())
    # print(getIdMaxCompetition())

    ################
    ################
    # DEMEER;Regis;15/07/1964;151229;FRANCE;ILE DE FRANCE Est;LE PERREUX;18742;20
    # requete1 = 'insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) values ("Test06/11/23","2023",True,0.2,"2023-11-06",2,5,1,5)'
    # cursor.execute(requete1)
    # db.commit()

    # requete2 = 'insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur,dateNaissanceTireur,nationTireur,comiteRegionalTireur) values ("DEEMER","Regis",151229,18742,1,"1964-07-15","FRANCE","ILE DE FRANCE Est")'
    # cursor.execute(requete2)
    # db.commit() 

    # requete3 = 'insert into TIREUR_DANS_COMPETITIONS() values (151229,4)'
    # cursor.execute(requete3)
    # db.commit()

    #print(getTournoisClosedParticiper(151229))
    #Pour réussir ce test il faut enlever le trigger sur la date inscription 

    #print(getListTournoisAllCLosed())
    # print(trieArchive("Sabre","none","none","none"))
    # print(getListTournoisAllCLosed())
    # print(trieArchive("Sabre","Homme","Senior","Loiret"))
    # print(getStatistique(151229))
    # print(infoCompetitionOuverte())
    # print(getInfoCompetition(1))
    # print(concourtNonFinitInscritTireur(151229))
    
    # print(getNbArbitre(2))
    # print(getNbTireur(2))
    pass
