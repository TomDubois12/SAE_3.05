import csv

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

#créer un curseur de base de données pour effectuer des opérations SQL
cursor = db.cursor()

def insertTireurDansCompetition(nom : str, prenom : str,numeroLicence : int ,classement : float, idSexe : int, dateNaissanceTireur : str, nation : str, comiteRegional : str, idCompetition: int) -> None:
    try :
        if estDansBDNational(numeroLicence) :
          insertTireurDansBD(numeroLicence)
          try :
            requete5 = "insert into TIREUR_DANS_COMPETITIONS (numeroLicenceTireur,idCompetition) values(%s,%s);"
            cursor.execute(requete5, (numeroLicence,idCompetition))
            db.commit()
          except Exception as mysql_error:
            print(mysql_error)
            return False
          return True  
        else : 
          return False
    except Exception as mysql_error:
      print(mysql_error)


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
      except Exception as mysql_error:
        print(mysql_error)

def corrigerDate(date :str) -> str : 
   newDate = date[6] + date[7] + date[8] + date[9] + "-" + date[3] + date[4] + "-" + date[0] + date[1]
   return newDate

def getInfoFromBDNational(numeroLicence : int) -> list :
  
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
    for cat in infoFichier :
       if str(numeroLicence) == cat[3] :
          return [f,cat]
  

def estDansBDNational(numeroLicence : int) -> bool:
  res = False
  fichiers = fichiersDossier("./escrimeFlask/csvEscrimeur/")
  for f in fichiers :
    infoFichier = classementFile("./escrimeFlask/csvEscrimeur/" + f)
    for cat in infoFichier :
       if str(numeroLicence) == cat[3] :
          return True
  return res 

def concourtInscritLicence(numeroLicence : int) -> list:
  requete1 = "select * from TIREUR_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceTireur = " + str(numeroLicence) + ";"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = []
  for i in range(len(info)):
    requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement
                  from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                  where datediff(dateDebutCompetiton ,CURDATE()) > 14 and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
    cursor.execute(requete2) 
    res.append(cursor.fetchall())
  # return sous la forme : nomCompetition intituleCompet typeArme intituleSexe intituleCategorie departement
  return res



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


def inscriptionOuverte() -> list:
    requete1 = "select * from COMPETITION where datediff(dateDebutCompetiton, CURDATE()) > 14;"
    cursor.execute(requete1)
    info = cursor.fetchall()
    res = []
    for i in range(len(info)):
      
      requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
                    from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                    where datediff(dateDebutCompetiton ,CURDATE()) > 14 and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +";"
      cursor.execute(requete2) 
      res.append(cursor.fetchall())
                            # print(info[i][0]) #idCompetition
                            # print(info[i][1]) #NomCompetition
                            # print(info[i][2]) #saison
                            # print(info[i][3]) #estFinit
                            # print(info[i][4]) #coeficient
                            # print(info[i][5]) #dateDebutCompetiton
                            # print(info[i][6]) #idLieu
                            # print(info[i][7]) #idCategorie
                            # print(info[i][8]) #idSexe
                            # print(info[i][9]) #idArme
    return res

def getOrganisateurClub():
  requete1 = "select * from ORGANISATEURDANSCLUB natural join CLUB ;"
  cursor.execute(requete1)
  info = cursor.fetchall()
  res = dict()
  for i in range(len(info)):
    res[info[i][1]] = info[i][2]
  return res


# def getProfil(numeroLicence : int) -> list:
#   requete1 = """select nomTireur, prenomTireur, dateNaissanceTireur, numeroLicenceTireur,  nationTireur, comiteRegionalTireur,nomCLub
#                 from TIREUR natural join TIREUR_DANS_CLUB natural join CLUB where numeroLicenceTireur = """ + str(numeroLicence) + " limit 1;"
#   cursor.execute(requete1)
#   res = []
#   res.append(cursor.fetchone())
#   return res



def fichiersDossier(path : str) :
  files = os.listdir(path)
  listeChemin = []
  for name in files:
    listeChemin.append(name)
  return listeChemin

if __name__ == "__main__":
    #print(classementFile("./csvEscrimeur/classement_Epée_Dames_M15.csv"))
    #print(inscriptionOuverte())
    #print(insertTireurCompetition("Nicolas", "Guillaume", 146313, 2452.00, 1,"2004-10-10","France","CENTRE VAL DE LOIRE", 1))
    #print(concourtInscritLicence(521531))
    #print(getOrganisateurClub())
    #print(getProfil(315486))
    #print(estDansBDNational(521531))
    #print(estDansBDNational(138932))
    #insertTireurDansCompetition(53985)

    pass

