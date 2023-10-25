import csv

# pip install Flask-MySQLdb
#sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config


# -*- coding: utf-8 -*-
import mysql.connector

#connexion au base de données
db = mysql.connector.connect(
  host = "localhost",
  user = "koko",
  password = "koko",
  database = "Escrime"
)

#créer un curseur de base de données pour effectuer des opérations SQL
c = db.cursor()

def insertTireurCompetition(nom,prenom,numeroLicence,classement,idSexe,idCompetition):
    try :
          requete2 = "insert into TIREUR (nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur) values(%s,%s,%s,%s,%s); "
          c.execute(requete2, (nom,prenom,numeroLicence,classement,idSexe))
          db.commit()
          try : 
            requete5 = "insert into TIREUR_DANS_COMPETITIONS (numeroLicenceTireur,idCompetition) values(%s,%s); "
            c.execute(requete5, (numeroLicence,idCompetition))
            db.commit()  
          except Exception as mysql_error:
            print(mysql_error)
    except Exception as mysql_error:
       print(mysql_error)


def classementFile(filename): 
    # à faire 
    with open(filename, 'r') as file :
        pass
    pass

def inscriptionOuverte(): 
    requete1 = "select * from COMPETITION where datediff(dateDebutCompetiton ,CURDATE()) > 14;"
    c.execute(requete1)
    info =  c.fetchall()
    res = []
    for i in range(len(info)):
      requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition 
                    from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
                    where datediff(dateDebutCompetiton ,CURDATE()) > 14 and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +";"
      c.execute(requete2) 
      res.append(c.fetchall())
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


if __name__ == "__main__":
    print(inscriptionOuverte())
