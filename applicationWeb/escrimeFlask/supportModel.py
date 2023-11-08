import csv
try :
    from .models import *
except Exception : 
    from models import *
    
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

cursor = db.cursor()

#  arme

def getIdLieuByNom(nomLieu): 
    try :
        requete = "select idLieu from LIEU where comiteReg = '" + str(nomLieu) +"' ;"
        cursor.execute(requete)
        return cursor.fetchall()[0][0]
    except Exception : 
        return None

def setNewLieuByNom(nomLieu): 
    requete = "insert into LIEU(adresse,region,departement,comiteReg) values('','','', '" + str(nomLieu) + "' )"
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


if __name__ == "__main__":
    # print(getIdLieuByNom("GRAND EST"))
    # print(getIidCategorieByNom("'U13'"))
    # print(getIdSexeByNom("'Homme'"))
    # print(getIdArmeByNom("'Fleuret'"))
    # print(getIdClubByNom("'EscriClub'"))
    pass 