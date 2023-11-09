import csv
try: 
  from .supportModel import *
except ImportError:
  from supportModel import *


# pip install Flask-MySQLdb
#sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config


import os.path

# -*- coding: utf-8 -*-
import mysql.connector

#connexion au base de données
db = mysql.connector.connect(
  host = "localhost",
  user = "nathan",
  password = "nathan",
  database = "Escrime"
)
#Blabla2147
#créer un curseur de base de données pour effectuer des opérations SQL
cursor = db.cursor()

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

def getListTournoisAllCLosed():
  requete1 = "select * from COMPETITION where estFinie = True order by dateDebutCompetiton DESC;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  return infoCompetitionFinie(info)
  

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
  requete = "select * from ORGANISATEURCOMPETITION natural join COMPETITION  where licenseOrganisateur = " + numLicence + ";"
  cursor.execute(requete)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                 from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                where  idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  return res

def createCompetition(nomCompete, lieu, categorie, sexe, arme, coef, date ) : 
  if getIdLieuByNom(lieu) is None : setNewLieuByNom(lieu)
  requete1 = """insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) 
                values ('""" + str(nomCompete) + "'," + str(corrigerDate(date)[0:4]) + "," + "False" + "," + str(coef) + ",'" + str(corrigerDate(date)) + "'," + str(getIdLieuByNom(lieu)) + "," + str(getIdCategorieByNom(categorie))+ "," + str(getIdSexeByNom(sexe)) +"," + str(getIdArmeByNom(arme)) + ");"""
  cursor.execute(requete1)
  db.commit()

def archiverCompetition(idCompetition): 
  requete = "update COMPETITION set estFinie = True where idCompetition = " + idCompetition + ";"
  cursor.execute(requete)
  db.commit()

def lancerCompetition(idCompetition): 
  requete = "update COMPETITION set dateDebutCompetiton = CURDATE() where idCompetition = " + idCompetition + ";"
  cursor.execute(requete)
  db.commit()

def competitionEstFinie(idCompetition): 
  requete = "select estFinie from COMPETITION where idCompetition = " + idCompetition + " ;"
  cursor.execute(requete)
  return cursor.fetchall()

def competitionEstLancer(idCompetition): 
  requete = "select datediff(dateDebutCompetiton,CURDATE()) from COMPETITION where idCompetition = " + idCompetition + " ;"
  cursor.execute(requete)
  return cursor.fetchall() == 0

def fichiersDossier(path : str) :
  files = os.listdir(path)
  listeChemin = []
  for name in files:
    listeChemin.append(name)
  return listeChemin

if __name__ == "__main__":
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
    
    pass
