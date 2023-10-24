insert into LIEU(adresse,region,department)  values 
    ('Chemin des plantes, 45140 Ormes','Centre','Loiret'),
    ('13 bis boulevard du 15 aout 1944','Centre-Val de Loire','Loiret'),
    ('3 rue de la gare','Centre-Val de Loire','Loiret'),
    ("6 rue des combattant d'afrique du sud","Centre-Val de Loire","Loiret");

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
    ("Roger","Bertrand","241354"),
    ("Wolfart","Patrick","254612"),
    ("Duboise","Tomy","734212"),
    ("Well","Brian","468412");

insert into ORGANISATEURDANSCLUB(idOrganisateur, idClub) values 
    (1,1),
    (2,2),
    (3,3),
    (4,4);
   
insert into TIREUR(nomTireur,prenomTireur,numeroLicenceTireur,classement,idSexeTireur) values
    ("Georget","Korentin","315486",45534,1),
    ("Boissay","Robin","521531",7,1),
    ("Boissay","Nathan","213138",5689,1),
    ("Dubois","Tom","324832",12,1),
    ("Brion","Adèle","465486",43000,2);

insert into ARBITRE(nomArbitre,prenomArbitre,numeroLicenceArbitre) values 
    ("Orhant","Killian","654123"),
    ("Farcy","Adam","947613"),
    ("Boissay","Gatien","542446");

insert into COMPETITION(intituleCompet,saison,estFinie,coefficientCompetition,dateDebutCompetiton,idLieuCompetition,idCategorieCompetition,idSexeCompetition,idArmeCompetition) values
    ("Tounrois hivernale 2023","2023",False,0.2,"2023-12-14",2,5,1,5);

insert into TIREUR_DANS_COMPETITIONS(idTireur,idCompetition)values 
    (1,1),
    (2,1),
    (3,1);

insert into POULE(nomPoule,numeroPiste,idCompetition) values 
    ("Poule 1",1,1);
    
insert into TIREUR_DANS_POULE(idTireur,idPoule) values 
    (1,1),
    (2,1),
    (3,1);

insert into ARBITRE_DANS_COMPETITIONS(idArbitre,idCompetition) values 
    (1,1);

insert into ARBITRE_POULE(idArbitre,idPoule) values 
   (1,1);