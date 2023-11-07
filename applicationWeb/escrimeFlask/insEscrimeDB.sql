insert into LIEU(adresse,region,departement,comiteReg)  values 
    ('Chemin des plantes, 45140 Ormes','Centre','Loiret','NORMANDIE'),
    ('13 bis boulevard du 15 aout 1944','Centre-Val de Loire','Loiret','GRAND EST'),
    ('3 rue de la gare','Centre-Val de Loire','Loiret','AUVERGNE RHONE ALPES'),
    ("6 rue des combattant d'afrique du sud","Centre-Val de Loire","Loiret",'ILE DE FRANCE Ouest');

insert into CATEGORIE(intituleCategorie) values 
    ('U13'),
    ('U15'),
    ('U17'),
    ('U20'),
    ('senior'),
    ('V1'),
    ('V2'),
    ('V3'),
    ('V4');

insert into ARME(typeArme,descriptionArme) values 
    ('fleuret homme','fleuret'),
    ('fleuret femme','fleuret'),
    ('épée homme','épée'),
    ('épée femme','épée'),
    ('sabre homme','sabre'),
    ('sabre femme','sabre');
 
insert into SEXE(intituleSexe) values
    ('Homme'),
    ('Femme');

insert into CLUB(nomClub) values 
    ('EscriClub'),
    ('EscriNais'),
    ("EscrimeClubBoulay"),
    ('EscrimeClubPatay');

insert into ORGANISATEUR(nomOrganisateur,prenomOrganisateur,licenseOrganisateur) values
    ("Roger","Bertrand",241354),
    ("Wolfart","Patrick",254612),
    ("Duboise","Tomy",734212),
    ("Well","Brian",468412);

insert into ORGANISATEURDANSCLUB(licenseOrganisateur, idClub) values 
    (241354,1),
    (254612,2),
    (734212,3),
    (468412,4);
   
insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur,dateNaissanceTireur,nationTireur,comiteRegionalTireur) values
    ("Georget","Korentin",315486,45534,1,'2004-05-23','France','CENTRE VAL DE LOIRE'),
    ("Boissay","Robin",521531,7,1,'2004-12-14','France','CENTRE VAL DE LOIRE'),
    ("Boissay","Nathan",213138,5689,1,'2004-12-14','France','CENTRE VAL DE LOIRE'),
    ("Dubois","Tom",324832,12,1,'2004-06-02','France','CENTRE VAL DE LOIRE'),
    ("Brion","Adèle",465486,43000,2,'2003-10-30','France','CENTRE VAL DE LOIRE'),
    ("DEEMER","Regis",151229,18742,1,"1964-07-15","FRANCE","ILE DE FRANCE Est");

insert into TIREUR_DANS_CLUB(numeroLicenceTireur,idClub) values 
    (315486,3),
    (521531,3),
    (213138,3);

insert into ARBITRE(nomArbitre,prenomArbitre,numeroLicenceArbitre) values 
    ("Orhant","Killian",654123),
    ("Farcy","Adam",947613),
    ("Boissay","Gatien",542446);

insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) values
    ("Tournois hivernale 2023","2023",False,0.2,"2023-12-14",2,5,1,5),
    ("Tournois hivernale 2024","2024",False,0.2,"2024-12-14",2,5,1,5),
    ("Tournois hivernale 2022","2022",True,0.2,"2022-12-14",2,5,1,5),

    ("Tournois printemps 2020","2020",True,0.2,"2020-11-14",1,5,1,5),
    ("Tournois automn 2020","2020",True,0.2,"2020-04-14",2,5,1,5),
    ("Tournois hiver 2020","2020",True,0.4,"2020-12-23",3,5,1,5),
    ("Tournois été 2020","2020",True,0.2,"2020-07-22",4,5,2,4),

    ("Tournois printemps 2021","202",True,0.2,"2021-11-14",2,1,1,5),
    ("Tournois automn 2021","2021",True,0.2,"2021-04-14",2,2,1,5),
    ("Tournois hiver 2021","2021",True,0.4,"2021-12-23",2,3,1,5),
    ("Tournois été 2021","2021",True,0.2,"2021-07-22",2,4,2,4),

    ("Tournois printemps 2019","2019",True,0.2,"2019-11-14",2,1,1,5),
    ("Tournois automn 2019","2019",True,0.2,"2019-04-14",2,2,2,2),
    ("Tournois hiver 2019","2019",True,0.4,"2019-12-23",2,3,2,6),
    ("Tournois été 2019","2019",True,0.2,"2019-07-22",2,4,2,4);


insert into TIREUR_DANS_COMPETITIONS(numeroLicenceTireur,idCompetition)values 
    (315486,1),
    (315486,2),
    (521531,1),
    (151229,4),
    (151229,5),
    (151229,6),
    (213138,1);
    

insert into POULE(nomPoule,numeroPiste,idCompetition) values 
    ("Poule 1",1,1);
    
insert into TIREUR_DANS_POULE(numeroLicenceTireur,idPoule) values 
    (315486,1),
    (521531,1),
    (213138,1);

insert into ARBITRE_DANS_COMPETITIONS(numeroLicenceArbitre,idCompetition) values 
    (654123,1);

insert into ARBITRE_POULE(numeroLicenceArbitre,idPoule) values 
   (654123,1);