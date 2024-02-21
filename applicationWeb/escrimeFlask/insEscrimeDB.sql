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
    ('Senior'),
    ('V1'),
    ('V2'),
    ('V3'),
    ('V4');

insert into ARME(typeArme,descriptionArme) values 
    ('Fleuret','Fleuret'),
    ('Épée','Épée'),
    ('Sabre','Sabre');
 
insert into SEXE(intituleSexe) values
    ('Homme'),
    ('Dames');

insert into CLUB(nomClub) values 
    ('EscriClub'),
    ('ISSY MOUSQUE'),
    ('ANTONY'),
    ('BLR92'),
    ('CE RUEIL'),
    ('NICE OGC'),
    ('LYON SE'),
    ('MELUN VDS'),
    ('TEAM FLEURET'),
    ('PAYS AIX'),
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
    ("Forfeit","Forfeit",0,0,1,'2000-01-01','Forfeit','Forfeit'),
    ("Boissay","Robin",521531,7,1,'2004-12-14','France','CENTRE VAL DE LOIRE'),
    ("Boissay","Nathan",213138,5689,1,'2004-12-14','France','CENTRE VAL DE LOIRE'),
    ("Dubois","Tom",324832,12,1,'2004-06-02','France','CENTRE VAL DE LOIRE'),
    ("Brion","Adèle",465486,43000,2,'2003-10-30','France','CENTRE VAL DE LOIRE'),
    
    ("teste","testee",151230,152412,1,'2003-11-30','France','CENTRE VAL DE LOIRE'),
    ("DEEMER","Regis",151229,18742,1,"1964-07-15","FRANCE","ILE DE FRANCE Est");

insert into TIREUR_DANS_CLUB(numeroLicenceTireur,idClub) values 
    (315486,3),
    (521531,3), 
    (151229,1),
    (151230,1),
    (213138,3);

-- insert into ARBITRE(nomArbitre,prenomArbitre,numeroLicenceArbitre) values 
--     ("Orhant","Killian",654123),
--     ("Farcy","Adam",947613),
--     ("Boissay","Gatien",542446);

insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) values
    ("Tournois hivernale 2023","2023",False,0.2,"2023-12-14",2,5,1,1),
    ("Tournois hivernale 2024","2024",False,0.2,"2024-12-14",2,5,1,2),
    ("Tournois hivernale 2022","2022",True,0.2,"2022-12-14",2,5,1,3),

    ("Tournois printemps 2020","2020",True,0.2,"2020-11-14",1,5,1,1),
    ("Tournois automn 2020","2020",True,0.2,"2020-04-14",2,5,1,2),
    ("Tournois hiver 2020","2020",True,0.4,"2020-12-23",3,5,1,3),
    ("Tournois été 2020","2020",True,0.2,"2020-07-22",4,5,2,1),

    ("Tournois printemps 2021","202",True,0.2,"2021-11-14",2,1,1,2),
    ("Tournois automn 2021","2021",True,0.2,"2021-04-14",2,2,1,3),
    ("Tournois hiver 2021","2021",True,0.4,"2021-12-23",2,3,1,1),
    ("Tournois été 2021","2021",True,0.2,"2021-07-22",2,4,2,2),

    ("Tournois printemps 2019","2019",True,0.2,"2019-11-14",2,1,1,3),
    ("Tournois automn 2019","2019",True,0.2,"2019-04-14",2,2,2,1),
    ("Tournois hiver 2019","2019",True,0.4,"2019-12-23",2,3,2,2),
    ("Tournois été 2019","2019",True,0.2,"2019-07-22",2,4,2,3);

insert into ORGANISATEURCOMPETITION(idCompetition, licenseOrganisateur) values 
    (1,241354),
    (2,254612),
    (3,734212),
    (4,468412),
    (5,241354),
    (6,254612),
    (7,254612),
    (8,254612),
    (9,254612),
    (10,254612),
    (11,254612),
    (12,254612),
    (13,241354),
    (14,254612),
    (15,734212);

insert into EQUIPE(idCompetition, nomEquipe, licenceChefEquipe) value 
    (17,"Les 1", 4029),
    (17,"Les 2", 241387),
    (17,"Les 3", 605),
    (17,"Les 4", 31646);

insert into TIREUR_EQUIPE(idEquipe, licenceTireur) value 
    (9, 45243),
    (9, 20840),
    (9, 53089),
    (9, 40845);

-- insert into TIREUR_DANS_COMPETITIONS(numeroLicenceTireur,idCompetition)values 
--     (315486,1),
--     (315486,2),
--     (521531,1),
--     (151229,4),
--     (151229,5),
--     (151229,6),
--     (151229,1),
--     (151230,1),
--     (213138,1);
    
-- insert into ARBITRE_DANS_COMPETITIONS(numeroLicenceArbitre,idCompetition) values 
--     (654123,1);

-- insert into POULE(nomPoule,numeroPiste,idCompetition) values 
--     ("Poule 1",1,1),
--     ("Poule 2",1,1);
    
-- insert into TIREUR_DANS_POULE(numeroLicenceTireur,idPoule) values 
--     (315486,1),
--     (521531,1),
--     (151229,2),
--     (213138,1);

-- insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule,toucheDTireur1,toucheDTireur2) value (
--     "Match12",
--     315486,
--     521531,
--     1,
--     1,
--     5,
--     0
-- );
-- insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule,toucheDTireur1,toucheDTireur2) value (
--     "Match23",
--     521531,
--     213138,
--     1,
--     1,
--     4,
--     5
-- );
-- insert into MATCHPOULE(nomMatchPoule,licenceTireur1,licenceTireur2,nbPhases,idPoule,toucheDTireur1,toucheDTireur2) value (
--     "Match13",
--     315486,
--     213138,
--     1,
--     1,
--     2,
--     5
-- );


-- insert into ARBITRE_POULE(numeroLicenceArbitre,idPoule) values 
--    (654123,1);