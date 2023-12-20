import csv
# pip install Flask-MySQLdb
#sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
from operator import itemgetter
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

def setNewClub(nomClub):
  req = "insert into CLUB (nomClub) value('"+str(nomClub)+"');"
  cursor.execute(req)
  db.commit()

def setTireurDansClub(licT, nomClub): 
  idClub = getIdClubByNom(nomClub)
  req = "insert into TIREUR_DANS_CLUB (numeroLicenceTireur,idClub) value("+str(licT)+",'"+str(idClub)+"');"
  cursor.execute(req)
  db.commit()

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

def clubExist(nomClub) :
  requete = "select * from CLUB where nomCLub = '" + str(nomClub) +"' ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  return len(res) == 1

def tireurDansClub(licenceTireur) :
  requete = "select * from TIREUR_DANS_CLUB where numeroLicenceTireur = " + str(licenceTireur) +" ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  return len(res) > 0

########################################################################
########################################################################
########################################################################
########################################################################
######################################################################## 

# On gère les orga ici 

def getInfoOrgaFromBDNational() -> list :
  return classementFile("./escrimeFlask/csvOrga/orga.csv")
   
def orgaDansClub(licOrga, nomClub) :    
  idClub = getIdClubByNom(nomClub)
  requete = "select * from CLUB natural join ORGANISATEURDANSCLUB where idClub = '" + str(idClub) +"' and licenseOrganisateur = "+str(licOrga) + " ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  return len(res) == 1

def setOrgaDansClub(licenceOrga, nomClub) : 
  if clubExist(nomClub) == False :
    setNewClub(nomClub)
  if orgaDansClub(licenceOrga, nomClub) == False :
    idClub = getIdClubByNom(nomClub) 
    requete5 = "insert into ORGANISATEURDANSCLUB (licenseOrganisateur,idClub) values(%s,%s);"
    cursor.execute(requete5, (licenceOrga, idClub))
    db.commit()

def insOrgaDansBD() : 
  listeOrga = getInfoOrgaFromBDNational()
  for orga in listeOrga : 
    requete5 = "insert into ORGANISATEUR (nomOrganisateur,prenomOrganisateur, licenseOrganisateur) values(%s,%s,%s);"
    cursor.execute(requete5, (orga[0],orga[1], orga[3]))
    db.commit()
    setOrgaDansClub(orga[3], orga[6])

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
        # = [idsexe] ['PETIT', 'Stéphane', '02/09/1963', '138932', 'FRANCE', 'ILE DE FRANCE Ouest', 'NEUILLY ESCR', '1687', '149']
        infoTireur = infoTireurGlobal[1]
        idSexe = infoTireurGlobal[0]

        

        if "Dames" in str(idSexe) : 
           idSexe = 2
        else : 
           idSexe = 1
        requete1 = "insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur,dateNaissanceTireur,nationTireur,comiteRegionalTireur) values(%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(requete1, (infoTireur[0],infoTireur[1],numeroLicence,infoTireur[7],idSexe,corrigerDate(infoTireur[2]),infoTireur[4],infoTireur[5]))
        db.commit()

        if clubExist(infoTireur[6]) == False :
          setNewClub(infoTireur[6])

        if tireurDansClub(infoTireur[3]) == False :
          setTireurDansClub(infoTireur[3],infoTireur[6])
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
  print(categorie)
  if (categorie == 'Vétérans3' or categorie == 'Vétérans4') and arme == "Epée" and sexe == "Homme" : 
      print("ici")
      return classementFile("./escrimeFlask/csvEscrimeur/classement_" + arme + "_" + sexe + "_" + categorie +".csv")
  elif categorie == 'Vétérans3' or categorie == 'Vétérans4' : 
    print("la")
    return classementFile("./escrimeFlask/csvEscrimeur/classement_" + arme + "_" + sexe + "_Vétérans3-4.csv")
  else : 
    print("pas la")
    return classementFile("./escrimeFlask/csvEscrimeur/classement_" + arme + "_" + sexe + "_" +categorie+ ".csv")
  
#print(getClassementNationnal("Epée","Femme","Vétérans3"))
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

def lancerCompetitionDate(idCompetition): 
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

def getNbPhase(idCompetition) :
  requete = "select max(nbPhases) from MATCHELIMINATION where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  nb = cursor.fetchall()
  if nb[0][0] == None : 
    return 1
  else :
    return nb[0][0]

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

def getNumeroLicenceArbitres(idCompetition):
  requete = "select numeroLicenceArbitre from COMPETITION natural join ARBITRE_DANS_COMPETITIONS where idCompetition = " + str(idCompetition) + " ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  liste = []
  for elem in res : 
    liste.append(elem[0])
  return liste

def estParticipant(numeroLicence, idCompetition) : 
  requete = "select * from COMPETITION natural join TIREUR_DANS_COMPETITIONS where idCompetition = " + str(idCompetition) + " and numeroLicenceTireur = " + str(numeroLicence) + " ;"
  cursor.execute(requete)
  return cursor.fetchall() != []

def getIdPouleTireur(numLicenceTireur, idCompetition) : 
  requete = "select idPoule from POULE natural join TIREUR_DANS_POULE where numeroLicenceTireur = " + str(numLicenceTireur) + "  and idCompetition = " +str(idCompetition) + ";"
  cursor.execute(requete)
  return cursor.fetchall()[0][0]

def getIdMatchElim(numLicenceTireur, idCompetition, nbPhases) : 
  requete = "select idMatchElimination from MATCHELIMINATION where nbPhases = " + str(nbPhases) +" and (licenceTireur1 = " + str(numLicenceTireur) + " OR licenceTireur2 = " +str(numLicenceTireur)+ ") and idCompetition = " +str(idCompetition) + ";"
  cursor.execute(requete)
  res=cursor.fetchall()[0][0]
  print('\033[90m' + str(res) + '\033[0m')
  return res

def getIdPouleArbitre(numLicenceArbitre, idCompetition) :
  requete = "select idPoule from POULE natural join ARBITRE_POULE where numeroLicenceArbitre = " + str(numLicenceArbitre) + " and idCompetition = " +str(idCompetition) + " ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  liste=[]
  for elem in res : 
    liste.append(elem[0])
  return liste

def getIdPouleOrganisateur(idCompetition) :
  requete = "select idPoule from POULE where idCompetition = " +str(idCompetition) + " ;"
  cursor.execute(requete)
  res = cursor.fetchall()
  liste=[]
  for elem in res : 
    liste.append(elem[0])
  return liste

def getNomByLicence(licence) : 
  requete = "select nomTireur, prenomTireur from TIREUR  where numeroLicenceTireur = " + str(licence) + ";"
  cursor.execute(requete)
  res = cursor.fetchall()[0]
  return res[0], res[1]

def getListNomByLicence(licences) : 
  res = []
  for lic in licences : 
    requete = "select nomTireur, prenomTireur, numeroLicenceTireur from TIREUR  where numeroLicenceTireur = " + str(lic) + ";"
    cursor.execute(requete)
    r = cursor.fetchall()[0]
    res.append((r[0],r[1],r[2]))
  return res

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

def getClassementApresPoule(idCompetition):
  requete = "select numeroLicenceTireur from TIREUR_DANS_POULE natural join POULE where idCompetition ="+ str(idCompetition) +  " order by nbVictoire DESC, TDMTR DESC  ;"
  cursor.execute(requete)
  l1 = cursor.fetchall()
  listeTrie = []
  for elem in l1 : 
    listeTrie.append(elem[0]) 
  return listeTrie

def getClassementPhase(idCompetition): 
  requete = "select numeroLicenceTireur from TIREUR_DANS_POULE natural join POULE where idCompetition ="+ str(idCompetition) +  " order by nbVictoire DESC, TDMTR DESC  ;"
  cursor.execute(requete)
  l1 = cursor.fetchall()
  listeTrie = []
  for elem in l1 : 
    listeTrie.append(elem[0]) 
  return listeTrie

def trierCeClass(classement,idComp,nbPhase) : 
  ran = [[2,3,4],[4,7,3],[8,15,2]]
  if nbPhase==5:
    classementFinit = [classement[0], classement[1]]
    listeT = []
    for ind in ran :
      listeT2 = []
      for i in range(0,ind[1] - ind[0] +1) :
        listeT.append(classement[ind[0] + i])
      for licence in listeT : 
        requete = "select licenceTireur1, toucheDTireur1, licenceTireur2, toucheDTireur2 from MATCHELIMINATION where idCompetition = "+str(idComp)+" and nbPhases = "+str(ind[2])+" and (licenceTireur1 = "+str(licence)+" OR licenceTireur2 = "+str(licence)+") ;"
        cursor.execute(requete)
        l2 = cursor.fetchall()
        lt1 = l2[0][0]
        lt2 = l2[0][2]
        td1 = l2[0][1]
        td2 = l2[0][3]
        if lt1 == licence : 
          listeT2.append((lt1,td1))
        elif lt2 == licence : 
          listeT2.append((lt2,td2))
      listeT2 = sorted(listeT2, key=lambda touche: touche[1])
      listeT2 = listeT2[::-1]
      for elem in listeT2 :
        classementFinit.append(elem[0])
      listeT = []
    print('\033[91m' + str(classementFinit) + '\033[0m')
    return classementFinit
  else:
    return []

def classementFinale(idCompetition,nbPhase) :
  classement = []
  liste16Meilleur = getClassementApresPoule(idCompetition)[:16]
  requete = "select * from MATCHELIMINATION where idCompetition = 1 order by nbPhases DESC"
  cursor.execute(requete)
  l1 = cursor.fetchall()
  for i in range(len(l1)) :

    lt1 = l1[i][2]
    lt2 = l1[i][4]
    td1 = l1[i][3]
    td2 = l1[i][5]
    if lt1 in liste16Meilleur and lt2 in liste16Meilleur :
      if td1 > td2 : 
        classement.append(lt1)
        classement.append(lt2)
        liste16Meilleur.remove(lt1)
        liste16Meilleur.remove(lt2)
      else : 
        classement.append(lt2)
        classement.append(lt1)
        liste16Meilleur.remove(lt2)
        liste16Meilleur.remove(lt1)
    elif lt1 in liste16Meilleur : 
      classement.append(lt1)
      liste16Meilleur.remove(lt1)
    elif lt2 in liste16Meilleur:
        classement.append(lt2)
        liste16Meilleur.remove(lt2)

  classement = trierCeClass(classement,idCompetition,nbPhase)
  classement += getClassementApresPoule(idCompetition)[16:]
  ind = 1 
  listeRenvoi = []
  for licence in classement :
    
    listeRenvoi.append([ind,getInfoFromBDNational(licence)[1][0],getInfoFromBDNational(licence)[1][1],getInfoFromBDNational(licence)[1][5],getInfoFromBDNational(licence)[1][6],getInfoFromBDNational(licence)[1][7],licence ])
    ind += 1
  print('\033[91m' + str(listeRenvoi) + '\033[0m')
  return listeRenvoi

def monClassementAMoi(idCompetition, licence, nbPhase) : 
  liste = classementFinale(idCompetition,nbPhase)
  for elem in liste : 
    if elem[6] == licence : 
      return elem

def getListeGagnantMatchElimination(nbPhase, idCompetition) : 
  requete = "select licenceTireur1, toucheDTireur1, licenceTireur2, toucheDTireur2 from MATCHELIMINATION  where idCompetition ="+ str(idCompetition) +  " and nbPhases = "+ str(nbPhase)+  "  ;"
  cursor.execute(requete)
  l1 = cursor.fetchall()
  listeTrie = []
  for elem in l1 : 
    if elem[1] == 5 : 
      listeTrie.append(elem[0]) 
    elif elem[3] == 5 :
      listeTrie.append(elem[2])

  return listeTrie


def getListeToucheByListLicence(listelisteLicence, nbPhases, idCompetition) : 
  listeTouche = []
  for i in range(len(listelisteLicence)): listeTouche.append([])
  ind = 0
  for listeLicence in listelisteLicence :
    for licence in listeLicence:
      requete = " select distinct licenceTireur1, toucheDTireur1, licenceTireur2, toucheDTireur2 from MATCHELIMINATION where idCompetition = "+ str(idCompetition) +" and nbPhases = "+str(ind + 2)+" and (licenceTireur1 = "+str(licence)+" or licenceTireur2 = "+str(licence)+");"
      cursor.execute(requete)
      l1 = cursor.fetchall()
      print(l1,licence)
      if len(l1) != 0 : 
        if l1[0][0] == licence :
          if l1[0][1] == -1 : listeTouche[ind].append(0)
          else : listeTouche[ind].append(l1[0][1])
          
        else :
          if l1[0][3] == -1 : listeTouche[ind].append(0)
          else : listeTouche[ind].append(l1[0][3])
      else :
        listeTouche[ind].append(0)
    ind += 1
  return listeTouche

def genererPhase(nbPhase, idCompetition,listeLicMatchACreer):
  if nbPhase == 2 :
    for k in range(int(len(listeLicMatchACreer)/2)) : 
        if listeLicMatchACreer[k*2] == 0 :
          idPoule = getIdPouleTireur(listeLicMatchACreer[k*2+1])
          nomMatch = "Match élimination: " + str(getNomByLicence(0)[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
          req = "insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(0)+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ",0,5);"
          cursor.execute(req)
          db.commit()
        elif listeLicMatchACreer[k*2+1] == 0 : 
          idPoule = getIdPouleTireur(listeLicMatchACreer[k*2])
          nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(0)[0])
          req = "insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(0)+" , "+ str(nbPhase)+" , " +str(idPoule) +  ",5,0);"
          cursor.execute(req)
          db.commit()
        else :
          nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
          idPoule = getIdPouleTireur(listeLicMatchACreer[k*2])
          req = "insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idPoule) +  ");"
          cursor.execute(req)
          db.commit()

  else : 
    for k in range(int(len(listeLicMatchACreer)/2)) : 
        if listeLicMatchACreer[k*2] == 0 :
          nomMatch = "Match élimination: " + str(getNomByLicence(0)[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
          req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(0)+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ",0,5);"
          cursor.execute(req)
          db.commit()
        elif listeLicMatchACreer[k*2+1] == 0 : 
          nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(0)[0])
          req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(0)+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ",5,0);"
          cursor.execute(req)
          db.commit()
        else :
          nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
          req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ");"
          cursor.execute(req)
          db.commit()


def maFonctionTropBelle(nbPhase, idCompetition,listeLicMatchACreer): 
  
  for k in range(int(len(listeLicMatchACreer)/2)) : 
    if listeLicMatchACreer[k*2] == 0 :
      nomMatch = "Match élimination: " + str(getNomByLicence(0)[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
      req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(0)+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ",0,5);"
      cursor.execute(req)
      db.commit()
    elif listeLicMatchACreer[k*2+1] == 0 : 
      nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(0)[0])
      req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition,toucheDTireur1,toucheDTireur2) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(0)+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ",5,0);"
      cursor.execute(req)
      db.commit()
    else :
      nomMatch = "Match élimination: " + str(getNomByLicence(listeLicMatchACreer[k*2])[0])+ "-" + str(getNomByLicence(listeLicMatchACreer[k*2+1])[0])
      req = "insert into MATCHELIMINATION(nomMatchElimination,licenceTireur1,licenceTireur2,nbPhases,idCompetition) value ('" + str(nomMatch) +"' , " +str(listeLicMatchACreer[k*2])+ "," + str(listeLicMatchACreer[k*2+1])+" , "+ str(nbPhase)+" , " +str(idCompetition) +  ");"
      cursor.execute(req)
      db.commit()

def genererPhaseEliminations(idCompetition, nbPhase) :
    listeTireurClasser = getClassementApresPoule(idCompetition)[:16]
    pat = [1,16,5,12,7,10,4,13,3,14,8,9,6,11,2,15]
    huit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(16) : 
      try  :
        huit[i] = listeTireurClasser[pat[i]-1]
      except IndexError : 
        huit[i] = 0

    quart = [0,0,0,0,0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(2, idCompetition)
    for i in range(8) : 
      if huit[i*2] in listeVictorieux : 
        quart[i] = huit[i*2]
      else :
        quart[i] = huit[i*2+1]

    demie = [0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(3, idCompetition)
    for i in range(4) : 
      if quart[i*2] in listeVictorieux : 
        demie[i] = quart[i*2]
      else :
        demie[i] = quart[i*2+1]

    finale = [0,0]
    listeVictorieux = getListeGagnantMatchElimination(4, idCompetition)
    for i in range(2) : 
      if demie[i*2] in listeVictorieux : 
        finale[i] = demie[i*2]
      else :
        finale[i] = demie[i*2+1]

    match nbPhase : 
      case 2 : 
        maFonctionTropBelle(2, idCompetition,huit)
      case 3 : 
        maFonctionTropBelle(3, idCompetition,quart)
      case 4 : 
        maFonctionTropBelle(4, idCompetition,demie)
      case 5 : 
        maFonctionTropBelle(5, idCompetition,finale)
    
    return (pat,listeVictorieux,listeTireurClasser,huit,quart,demie,finale)

def affichageGenererPhaseEliminations(idCompetition, nbPhase) :
    listeTireurClasser = getClassementApresPoule(idCompetition)[:16]
    pat = [1,16,5,12,7,10,4,13,3,14,8,9,6,11,2,15]
    huit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(16) : 
      try  :
        huit[i] = listeTireurClasser[pat[i]-1]
      except IndexError : 
        huit[i] = 0

    quart = [0,0,0,0,0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(2, idCompetition)
    for i in range(8) : 
      if huit[i*2] in listeVictorieux : 
        quart[i] = huit[i*2]
      else :
        quart[i] = huit[i*2+1]

    demie = [0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(3, idCompetition)
    for i in range(4) : 
      if quart[i*2] in listeVictorieux : 
        demie[i] = quart[i*2]
      else :
        demie[i] = quart[i*2+1]

    finale = [0,0]
    listeVictorieux = getListeGagnantMatchElimination(4, idCompetition)
    for i in range(2) : 
      if demie[i*2] in listeVictorieux : 
        finale[i] = demie[i*2]
      else :
        finale[i] = demie[i*2+1]
    
    return (pat,listeVictorieux,listeTireurClasser,huit,quart,demie,finale)

def getNomPrenomMatchElimination(idCompetition) :
    listeTireurClasser = getClassementApresPoule(idCompetition)[:16]
    pat = [1,16,5,12,7,10,4,13,3,14,8,9,6,11,2,15]
    huit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(16) : 
      try  :
        huit[i] = listeTireurClasser[pat[i]-1]
      except IndexError : 
        huit[i] = 0

    quart = [0,0,0,0,0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(2, idCompetition)
    for i in range(8) : 
      if huit[i*2] in listeVictorieux : 
        quart[i] = huit[i*2]
      else :
        quart[i] = huit[i*2+1]

    demie = [0,0,0,0]
    listeVictorieux = getListeGagnantMatchElimination(3, idCompetition)
    for i in range(4) : 
      if quart[i*2] in listeVictorieux : 
        demie[i] = quart[i*2]
      else :
        demie[i] = quart[i*2+1]

    finale = [0,0]
    listeVictorieux = getListeGagnantMatchElimination(4, idCompetition)
    for i in range(2) : 
      if demie[i*2] in listeVictorieux : 
        finale[i] = demie[i*2]
      else :
        finale[i] = demie[i*2+1]

    gagnant = [0]
    listeVictorieux = getListeGagnantMatchElimination(5, idCompetition)
    if finale[0] in listeVictorieux : 
      gagnant[0] = finale[0]
    else :
      gagnant[0] = finale[1]

    # print(pat,listeVictorieux,listeTireurClasser,huit,quart,demie,finale)
    return [getListNomByLicence(huit),getListNomByLicence(quart),getListNomByLicence(demie),getListNomByLicence(finale),getListNomByLicence(gagnant)]

def setToucherDonneTireur(licenceTireur1, licenceTireur2, toucheDTireur, idCompetition, nbPhase) :
  if int(nbPhase) == 1:
    idPoule = getIdPouleTireur(licenceTireur1, idCompetition)
    requete = "select licenceTireur1 from MATCHPOULE where licenceTireur1 = " + str(licenceTireur1) + " and licenceTireur2 = " + str(licenceTireur2) + " and idPoule = " + str(idPoule) + ";"
    cursor.execute(requete)
    l1 = cursor.fetchall()
    print('\033[91m' + str(l1) + '\033[0m')
    if l1 != [] :
      requete = "update MATCHPOULE set toucheDTireur1 = " + str(toucheDTireur) + " where licenceTireur1 = " + str(licenceTireur1) + " and licenceTireur2 = " + str(licenceTireur2) + " and idPoule = " + str(idPoule) + " and nbPhases = "+ str(nbPhase) +";"
    else:
      requete = "update MATCHPOULE set toucheDTireur2 = " + str(toucheDTireur) + " where licenceTireur1 = " + str(licenceTireur2) + " and licenceTireur2 = " + str(licenceTireur1) + " and idPoule = " + str(idPoule) + " and nbPhases = "+ str(nbPhase) +";"      
    cursor.execute(requete)
    db.commit()
  else :
    # print('\033[90m' + str(nbPhase) +" " + licenceTireur1 + " " +  idCompetition + '\033[0m')
    idMatchElim = getIdMatchElim(licenceTireur1,idCompetition, nbPhase)
    # print(idMatchElim)
    # print('\033[91m' + str(idMatchElim) + " " + str(nbPhase)+ '\033[0m')
    requete = "select licenceTireur1 from MATCHELIMINATION where licenceTireur1 = " + str(licenceTireur1) + " and idMatchElimination = " + str(idMatchElim) + ";"
    cursor.execute(requete)
    l1 = cursor.fetchall()
    print('\033[91m' + str(l1) + '\033[0m')
    if l1 != [] :
      requete = "update MATCHELIMINATION set toucheDTireur1 = " + str(toucheDTireur) + " where licenceTireur1 = " + str(licenceTireur1) + " and idMatchElimination = " + str(idMatchElim) + " and nbPhases = "+ str(nbPhase) +";"
    else:
      requete = "update MATCHELIMINATION set toucheDTireur2 = " + str(toucheDTireur) + " where licenceTireur2 = " + str(licenceTireur1) + " and idMatchElimination = " + str(idMatchElim) + " and nbPhases = "+ str(nbPhase) +";"      
    cursor.execute(requete)
    db.commit()

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
  metAJourInfoTireurDansPoule(dico, idCompetition)
  liste=[]
  liste.append(dico)
  return liste

def InfosPouleNumLicenceArbitre(idCompetition, numLicenceArbitre) : 
  listeNumLicencePoule = []
  idPoule = getIdPouleArbitre(numLicenceArbitre, idCompetition)
  for idP in idPoule : 
    requete = "select distinct numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_POULE where idCompetition = "+ str(idCompetition) +" and idPoule = " + str(idP) + ";"
    cursor.execute(requete)
    res= cursor.fetchall()
    liste=[]
    for elem in res :
      liste.append(elem[0])
    listeNumLicencePoule.append(liste)

    # print(listeNumLicencePoule[t])
  # "select licenceTireur1,licenceTireur2, toucheDTireur1  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + idCompetition + "and numeroLicenceTireur = " + numLicenceTireur + " and licenceTireur1 = " + numLicenceTireur+";"
  final=[]
  for listeNumLicence in listeNumLicencePoule :
    dico = dict()
    for numLicence in listeNumLicence: 
      Lo = numLicence
      requete = "select distinct licenceTireur1,licenceTireur2, toucheDTireur1, toucheDTireur2  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + str(idCompetition) + " and ( numeroLicenceTireur = " + str(Lo) + " and licenceTireur1 = " + str(Lo)+") or ( licenceTireur2 = " + str(Lo)+") ;"
      cursor.execute(requete)
      res = cursor.fetchall()
      key = (Lo,listeNumLicence.index(Lo)+1)
      nom, prenom = getNomByLicence(Lo)
      club = getNomClubByLicence(Lo)
      listeMatch = []
      for j in range(len(res)) :
        if res[j][0] == Lo : 
          listeMatch.append((res[j][1],res[j][2],res[j][3]))
        else : 
          listeMatch.append((res[j][0],res[j][3],res[j][2]))
      listeMatch.reverse()
      listeMatch.insert(listeNumLicence.index(Lo),(Lo,-2,-2))
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

    final.append(dico)

  # print(dico)
  for dico in final :
    dico = classementPoule(dico)
    metAJourInfoTireurDansPoule(dico, idCompetition)
  return final

def InfosPouleSansLicence(idCompetition) : 
  listeNumLicencePoule = []
  idPoule = getIdPouleOrganisateur(idCompetition)
  for idP in idPoule : 
    requete = "select distinct numeroLicenceTireur from COMPETITION natural join TIREUR_DANS_POULE where idCompetition = "+ str(idCompetition) +" and idPoule = " + str(idP) + ";"
    cursor.execute(requete)
    res= cursor.fetchall()
    liste=[]
    for elem in res :
      liste.append(elem[0])
    listeNumLicencePoule.append(liste)

    # print(listeNumLicencePoule[t])
  # "select licenceTireur1,licenceTireur2, toucheDTireur1  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + idCompetition + "and numeroLicenceTireur = " + numLicenceTireur + " and licenceTireur1 = " + numLicenceTireur+";"
  final=[]
  for listeNumLicence in listeNumLicencePoule :
    dico = dict()
    for numLicence in listeNumLicence: 
      Lo = numLicence
      requete = "select distinct licenceTireur1,licenceTireur2, toucheDTireur1, toucheDTireur2  from COMPETITION natural join TIREUR_DANS_POULE natural join POULE natural join MATCHPOULE where idCompetition =" + str(idCompetition) + " and ( numeroLicenceTireur = " + str(Lo) + " and licenceTireur1 = " + str(Lo)+") or ( licenceTireur2 = " + str(Lo)+") ;"
      cursor.execute(requete)
      res = cursor.fetchall()
      key = (Lo,listeNumLicence.index(Lo)+1)
      nom, prenom = getNomByLicence(Lo)
      club = getNomClubByLicence(Lo)
      listeMatch = []
      for j in range(len(res)) :
        if res[j][0] == Lo : 
          listeMatch.append((res[j][1],res[j][2],res[j][3]))
        else : 
          listeMatch.append((res[j][0],res[j][3],res[j][2]))
      listeMatch.reverse()
      listeMatch.insert(listeNumLicence.index(Lo),(Lo,-2,-2))
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

    final.append(dico)

  # print(dico)
  for dico in final :
    dico = classementPoule(dico)
    metAJourInfoTireurDansPoule(dico, idCompetition)
  return final

def classementPoule(dico):
  #trier du 1 au dernier en fonction du nombre de victoire
  #si egalité, on regarde la différence de toucheDonnéeTotale - toucheRecuTotale

  #dico = (numLicence, num) : (nom,prenom,club,[(num,toucheDonnee,toucheRecu)], toucheDonnéeTotal, toucheRecuTotal)
  
  liste = []
  for key in dico.keys():
    liste.append(key)
  liste.sort(key=lambda x: (dico[x][6],dico[x][4]-dico[x][5]),reverse=True)
  for i in range(len(liste)):
    dico[liste[i]] = (dico[liste[i]][0],dico[liste[i]][1],dico[liste[i]][2],dico[liste[i]][3],dico[liste[i]][4],dico[liste[i]][5],dico[liste[i]][6],i+1)
  return dico

def calculer_nombre_poules(liste_choix_part_poule, nb_part, nb_arbitre):

  listeNbPoule = []
  
  if nb_part in liste_choix_part_poule : 
    return [nb_part,1,0]


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
  # print(listeIdPoule)
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
      inc = -1
    elif ind == -1 : 
      inc = 1

def insArbitreDansPoule(infosArbitre, idCompetition) : 
  nbArbitre = len(infosArbitre)
  listeIdPoule = getListeidPouleCompetition(idCompetition)
  nbPoule = len(listeIdPoule)
  ind = 0 #ind  idPoule
  i = 0  # ind infoTireur
  while nbPoule > 0 : 
    nbPoule -= 1 
    # print(infosArbitre,i,nbArbitre,listeIdPoule,ind)
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
  print(listeIdPoule)
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

def metAJourInfoTireurDansPoule(dico, idCompetition) : 
  #dico[key] = (nom,prenom,club,listeMatch,nbTotalTouchesDonnees,nbTotalTouchesRecues,victoire,0)
  for elem in dico.items() : 

    idPoule = getIdPouleTireur(elem[0][0], idCompetition)

    tdmtr = elem[1][4] - elem[1][5]
    nbVictoire = elem[1][6]
    placePoule = elem[1][7]
    requete = "update TIREUR_DANS_POULE set nbVictoire = " + str(nbVictoire) + ", placePoule = " + str(placePoule) + ", TDMTR = " + str(tdmtr) + " where idPoule = " + str(idPoule) + " and numeroLicenceTireur = " + str(elem[0][0]) + ";"      
    cursor.execute(requete)
    db.commit()
    print(elem[0] , tdmtr , placePoule,nbVictoire)
    pass

def lancerCompetition(idCompetition): 
  lancerCompetitionDate(idCompetition)
  nbTireur,nbArbitre = getNbTireur(idCompetition), getNbArbitre(idCompetition)
  #if nbTireur < 5 or nbArbitre == 0 : return None
  infosTireur, infosArbitre = getInfoTireurs(idCompetition), getInfoArbitres(idCompetition)

  # 1) gener nbPoule en fonction nbTIreur et Arbitre
  listeChoixPartPoule, listePoules = [5,6,7,8,9], []
  choixTPP, nbPoule, resteT   = calculer_nombre_poules(listeChoixPartPoule, nbTireur, nbArbitre)

  # pour le moment les tireurs ne sont pas mit dabs les poules c'est juste des testes pour voir si le model marche

  for i in range(nbPoule - 1 if choixTPP == 5 and resteT > 0 else nbPoule):
    listePoules.append([])

  print(choixTPP, nbPoule, resteT, nbTireur,listePoules)
  print(infosTireur)
  createPoule(idCompetition,len(listePoules))
  insTireurDansPoule(infosTireur, idCompetition)
  insArbitreDansPoule(infosArbitre, idCompetition)
  genererMatchPouleIdCompetition(idCompetition)



if __name__ == "__main__":
    # print(getNomByLicence(315486))
    # print(InfosPouleNumLicence(1,315486))
    # print(getListeidPouleCompetition(1))
    #print(getIdPouleTireur(315486))
    # print(calculer_nombre_poules([5,6,7,8,9], 7, 2))
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
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(getCompetitionParOrga(254612))
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(getProfil(151229))
    # print(getCompetitionParOrga(254612))
    # print(getClassementNationnal("Sabre","Dames","Seniors"))
    # print(getProfil(151229))
    # print(InfosPouleNumLicenceArbitre(1,51032))


    #################################
    # insertTireurDansBD(45243)
    # insertTireurDansBD(20840)
    # insertTireurDansBD(53089)
    # insertTireurDansBD(40845)
    # insertTireurDansBD(37189)
    # insertTireurDansBD(53998)
    # insertTireurDansBD(54797)
    # insertTireurDansBD(5387)
    # insertTireurDansBD(35524)
    # insertTireurDansBD(20981)
    # insertTireurDansBD(2889)
    # insertTireurDansBD(7006)
    # insertTireurDansBD(119662)
    # insertTireurDansBD(41337)
    # insertTireurDansBD(37332)
    # insertTireurDansBD(5529)
    # insertTireurDansBD(72333)
    # insertTireurDansBD(658)
    # insertTireurDansBD(34193)

    # test = [45243,20840,53089,40845,37189,53998,54797,5387,35524,20981,2889,7006,119662,41337,37332,5529,72333,658,34193]

    # for id in test : 
    #   requete5 = "insert into TIREUR_DANS_COMPETITIONS (numeroLicenceTireur,idCompetition) values("+str(id)+", 1  );"
    #   cursor.execute(requete5)
    #   db.commit()

    # insertArbitreDansBD(51032)
    # insertArbitreDansBD(51061)

    # test1 = [51032,51061]
    # for id in test1 : 
    #   requete5 = "insert into ARBITRE_DANS_COMPETITIONS (numeroLicenceArbitre,idCompetition) values("+str(id)+", 1  );"
    #   cursor.execute(requete5)
    #   db.commit()

    # print(lancerCompetition(1)) # Pour creer une competition pour les tests
    # insOrgaDansBD()
    ################

    # print(genererPhaseEliminations(1,2))
    # print(genererPhaseEliminations(1,3))
    #print(genererPhaseEliminations(1,5))
    # print(classementFinale(1))
    # print(monClassementAMoi(1, 5529))

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


    # # print(getNomPrenomMatchElimination(1)) # pour les nomETprenom

    # print(genererPhaseElimination(1,2)) # pour generer une phase et get liste avec licene
    # print(getListeToucheByListLicence([[53998, 119662, 5387, 658, 41337, 2889, 45243, 35524, 72333, 37332, 40845, 7006, 20981, 37189, 53089, 54797], [53998, 54797, 41337, 7006, 45243, 37332, 658, 20981, 5387, 37189, 35524, 72333, 2889, 40845, 119662, 53089], [54797, 7006, 37332, 20981, 37189, 72333, 40845, 53089], [7006, 20981, 72333, 53089], [20981, 53089]],2,1))


    #print(getListeToucheByListLicence([45243,20840,53089,40845,37189,53998,54797,5387,35524,20981], 2, 1))
    # genererPhase(1,3)
    # print(setToucherDonneTireur(5387, 20981, 5, 1, 4))
    # print(setToucherDonneTireur(35524, 53089, 5, 1, 4))
    # print(setToucherDonneTireur(53089, 20840, 5, 1, 3))
    # print(setToucherDonneTireur(35524, 54797, 5, 1, 3))
    # genererPhaseEliminations(1,5)
    # genererPhase(1,4)
    # print(genererPhaseEliminations(1,2))
    # # InfosPouleNumLicence(1, 20981)
    # # print(InfosPouleNumLicenceArbitre(1,51061))
    # # print(getClassementApresPoule(1))
    #print(getNomPrenomMatchElimination(1))
    # print(genererPhase(1,3))
    # print((getIdMatchElim(5387,1)))
    # print(setToucherDonneTireur(40845, 20981, -1, 1, 2))
    # print(getListeGagnantMatchElimination(2, 1))
    
    pass
