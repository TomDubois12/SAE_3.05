# import csv

# # pip install Flask-MySQLdb
# #sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config


# # -*- coding: utf-8 -*-
# import mysql.connector

# #connexion au base de données
# # db = mysql.connector.connect(
# #   host = "localhost",
# #   user = "nathan",
# #   password = "nathan",
# #   database = "Escrime"
# # )

# #créer un curseur de base de données pour effectuer des opérations SQL
# # cursor = db.cursor()

# def insertTireurCompetition(nom : str, prenom : str,numeroLicence : int ,classement : float, idSexe : int,dateNaissance : str, nationTireur : str, comiteRegional : str, idCompetition: int) -> None:
#     try :
#           requete2 = "insert into TIREUR (nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur, dateNaissanceTireur, nationTireur, comiteRegionalTireur) values(%s,%s,%s,%s,%s,%s,%s,%s);"
#           cursor.execute(requete2, (nom,prenom,numeroLicence,classement,idSexe,dateNaissance,nationTireur,comiteRegional))
#           db.commit()
#           try :
#             requete5 = "insert into TIREUR_DANS_COMPETITIONS (numeroLicenceTireur,idCompetition) values(%s,%s);"
#             cursor.execute(requete5, (numeroLicence,idCompetition))
#             db.commit()
#           except Exception as mysql_error:
#             print(mysql_error)
#     except Exception as mysql_error:
#        print(mysql_error)

# def concourtInscritLicence(numeroLicence : int) -> list:
#   requete1 = "select * from TIREUR_DANS_COMPETITIONS natural join COMPETITION where numeroLicenceTireur = " + str(numeroLicence) + ";"
#   cursor.execute(requete1)
#   info = cursor.fetchall()
#   res = []
#   for i in range(len(info)):
#     requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement
#                   from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
#                   where datediff(dateDebutCompetiton ,CURDATE()) > 14 and idLieu ="""+ str(info[i][7]) +" and idCategorie ="+ str(info[i][8]) +" and idSexe = "+str(info[i][9]) +" and idArme = "+ str(info[i][10]) +" and idCompetition = "+str(info[i][0]) +";"
#     cursor.execute(requete2) 
#     res.append(cursor.fetchall())
#   # return sous la forme : nomCompetition intituleCompet typeArme intituleSexe intituleCategorie departement
#   return res



# def classementFile(filename :str) -> list:
#     "nom prenom date_naissance adherent nation comite_regional club points rang"
#     res = []
#     with open(filename, 'r',encoding='Latin-1') as file :
#       next(file)
#       for ligne in file:
#         ligne = ligne.split(";")
#         ligne[8] = ligne[8].replace("\n","")
#         res.append(ligne)
#       file.close()
#     return res


# def inscriptionOuverte() -> list:
#     requete1 = "select * from COMPETITION where datediff(dateDebutCompetiton, CURDATE()) > 14;"
#     cursor.execute(requete1)
#     info = cursor.fetchall()
#     res = []
#     for i in range(len(info)):
      
#       requete2 = """select intituleCompet,typeArme, intituleSexe,intituleCategorie, departement, idCompetition
#                     from COMPETITION natural join LIEU natural join ARME natural join SEXE natural join CATEGORIE
#                     where datediff(dateDebutCompetiton ,CURDATE()) > 14 and idLieu ="""+ str(info[i][6]) +" and idCategorie ="+ str(info[i][7]) +" and idSexe = "+str(info[i][8]) +" and idArme = "+ str(info[i][9]) +" and idCompetition = "+str(info[i][0]) +";"
#       cursor.execute(requete2) 
#       res.append(cursor.fetchall())
#                             # print(info[i][0]) #idCompetition
#                             # print(info[i][1]) #NomCompetition
#                             # print(info[i][2]) #saison
#                             # print(info[i][3]) #estFinit
#                             # print(info[i][4]) #coeficient
#                             # print(info[i][5]) #dateDebutCompetiton
#                             # print(info[i][6]) #idLieu
#                             # print(info[i][7]) #idCategorie
#                             # print(info[i][8]) #idSexe
#                             # print(info[i][9]) #idArme
#     return res

# def getOrganisateurClub():
#   requete1 = "select * from ORGANISATEURDANSCLUB natural join CLUB ;"
#   cursor.execute(requete1)
#   info = cursor.fetchall()
#   res = dict()
#   for i in range(len(info)):
#     res[info[i][1]] = info[i][2]
#   return res

# if __name__ == "__main__":
#     #print(classementFile("./csvEscrimeur/classement_Epée_Dames_M15.csv"))
#     #print(inscriptionOuverte())
#     #print(insertTireurCompetition("Nicolas", "Guillaume", 145313, 2452.00,1,"2004-10-10" ,"France","CENTRE VAL DE LOIRE", 1))
#     #print(concourtInscritLicence(145313))
#     #print(getOrganisateurClub())
#     pass
