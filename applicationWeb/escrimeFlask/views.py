from flask import Flask

# pip install Flask-MySQLdb
#sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
app = Flask(__name__)

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
cur = db.cursor()

#requéte SQL
sql = "insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur) values('Nathan','Nathan','123458','125',1);"

cur.execute(sql)

#valider la transaction
db.commit()

#afficher le nombre de lignes insérées
print(cur.rowcount, "ligne insérée.")


# @app.route('/')
# def CONNECT_DB():
#     CS = mysql.connection.cursor()
#     Executed_DATA = ()
   

#     CS.execute("""insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur) values('Nathan','Nathan','123458','125',1);""")
    
#     CS.execute("""SELECT * FROM TIREUR""")  
#     Executed_DATA += CS.fetchall()

#     print(Executed_DATA)
#     res = ""
#     for data in Executed_DATA:
#         res+= str(data) + "\n\n"
    
#     return str(res)

# if __name__ == "__main__":
#     app.run(debug=True)

