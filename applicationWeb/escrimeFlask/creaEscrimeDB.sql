SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `Escrime` DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci;
USE `Escrime`;
-- not null auto_increment 


create table LIEU(
    idLieu int not null auto_increment,
    adresse varchar(100) not null,
    region varchar(50) not null,
    departement varchar(50) not null,
    comiteReg varchar(50) not null,
    primary key (idLieu)
);

create table CATEGORIE(
    idCategorie int not null auto_increment,
    intituleCategorie varchar(50) not null,
    primary key (idCategorie)
);

create table SEXE(
    idSexe int not null auto_increment,
    intituleSexe varchar(10) not null,
    primary key (idSexe)
    );

create table ARME(
    idArme int not null auto_increment,
    typeArme varchar(50) not null,
    descriptionArme varchar(100),
    primary key (idArme)
);

create table CLUB(
    idClub int not null auto_increment,
    nomClub varchar(50) not null,
    primary key (idClub)
);

create table ORGANISATEUR(
    nomOrganisateur varchar(50) not null,
    prenomOrganisateur varchar(50) not null,
    licenseOrganisateur int not null,
    primary key (licenseOrganisateur)
);

create table ORGANISATEURDANSCLUB(
    idClub int not null,
    licenseOrganisateur int not null,
    primary key (idClub, licenseOrganisateur),
    Foreign key(idCLub) references CLUB(idCLub),
    Foreign key(licenseOrganisateur) references ORGANISATEUR(licenseOrganisateur)
);

create table TIREUR(
    nomTireur varchar(50) not null,
    prenomTireur varchar(50) not null,
    numeroLicenceTireur int not null,
    classement Float(10,2) not null,
    idSexeTireur int not null, 
    dateNaissanceTireur date not null,
    nationTireur varchar(50) not null,
    comiteRegionalTireur varchar(50) not null, 
    primary key (numeroLicenceTireur),
    Foreign key(idSexeTireur) references SEXE(idSexe)
);

create table ARBITRE(
    nomArbitre varchar(30) not null,
    prenomArbitre varchar(30) not null,
    numeroLicenceArbitre int not null,
    primary key (numeroLicenceArbitre)
);

create table COMPETITION(
    idCompetition int not null auto_increment,
    intituleCompet varchar(42) not null,
    saison varchar(20) not null,
    estFinie boolean not null,
    coefficientCompetition Float(10,2) not null,
    dateDebutCompetiton date not null,
    idLieuCompetition int not null,
    idCategorieCompetition int not null,
    idSexeCompetition int not null,
    idArmeCompetition int not null,
    typeCompetition varchar(20) not null,
    primary key (idCompetition),
    Foreign key(idLieuCompetition) references LIEU(idLieu),
    Foreign key(idCategorieCompetition) references CATEGORIE(idCategorie),
    Foreign key(idSexeCompetition) references SEXE(idSexe),
    Foreign key(idArmeCompetition) references ARME(idArme)
);

create table ORGANISATEURCOMPETITION(
    idCompetition int not null,
    licenseOrganisateur int not null,
    primary key (idCompetition, licenseOrganisateur),
    Foreign key(idCompetition) references COMPETITION(idCompetition),
    Foreign key (licenseOrganisateur) references ORGANISATEUR(licenseOrganisateur)
);

create table MATCHELIMINATION(
    idMatchElimination int not null auto_increment,
    nomMatchElimination varchar(60),
    licenceTireur1 int not null,
    toucheDTireur1 int DEFAULT -1,
    licenceTireur2 int not null,
    toucheDTireur2 int DEFAULT -1,
    nbPhases int not null,
    numeroPiste int,
    idCompetition int not null,
    primary key (idMatchElimination),
    Foreign key(licenceTireur1) references TIREUR(numeroLicenceTireur),
    Foreign key(licenceTireur2) references TIREUR(numeroLicenceTireur),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table POULE(
    idPoule int not null auto_increment,
    nomPoule varchar(42) not null,
    numeroPiste int not null,
    idCompetition int not null,
    primary key(idPoule),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table MATCHPOULE(
    idMatchPoule int not null auto_increment,
    nomMatchPoule varchar(42) not null,
    licenceTireur1 int not null,
    toucheDTireur1 int DEFAULT -1,
    licenceTireur2 int not null,
    toucheDTireur2 int DEFAULT -1,
    nbPhases int not null,
    idPoule int not null,
    primary key(idMatchPoule),
    Foreign key(idPoule) references POULE(idPoule)
);

create table TIREUR_DANS_COMPETITIONS(
    numeroLicenceTireur int not null,
    idCompetition int not null,
    primary key (numeroLicenceTireur, idCompetition),
    Foreign key(numeroLicenceTireur) references TIREUR(numeroLicenceTireur),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table TIREUR_DANS_POULE(
    numeroLicenceTireur int not null,
    nbVictoire int not null DEFAULT 0 ,
    placePoule int,
    TDMTR int DEFAULT 0,
    idPoule int not null,
    primary key (numeroLicenceTireur, idPoule),
    Foreign key(numeroLicenceTireur) references TIREUR(numeroLicenceTireur),
    Foreign key(idPoule) references POULE(idPoule)
);

create table TIREUR_DANS_CLUB(
    numeroLicenceTireur int not null,
    idClub int not null,
    primary key (numeroLicenceTireur, idClub),
    Foreign key(numeroLicenceTireur) references TIREUR(numeroLicenceTireur),
    Foreign key(idClub) references CLUB(idClub)
);

create table ARBITRE_DANS_COMPETITIONS(
    numeroLicenceArbitre int not null,
    idCompetition int not null,
    primary key (numeroLicenceArbitre, idCompetition),
    Foreign key(numeroLicenceArbitre) references ARBITRE(numeroLicenceArbitre),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table ARBITRE_POULE(
    numeroLicenceArbitre int not null,
    idPoule int not null,
    primary key (numeroLicenceArbitre, idPoule),
    Foreign key(numeroLicenceArbitre) references ARBITRE(numeroLicenceArbitre),
    Foreign key(idPoule) references POULE(idPoule)
);

create table ARBITRE_ELIMINATION(
    numeroLicenceArbitre int not null,
    idMatchElimination int not null,
    primary key (numeroLicenceArbitre, idMatchElimination),
    Foreign key(numeroLicenceArbitre) references ARBITRE(numeroLicenceArbitre),
    Foreign key(idMatchElimination) references MATCHELIMINATION(idMatchElimination)
);


create table EQUIPE(
    idEquipe int not null auto_increment, 
    idCompetition int not null,
    nomEquipe varchar(255) not null, 
    licenceChefEquipe int not null,
    primary key (idEquipe, idCompetition),
    Foreign key(idCompetition) references COMPETITION(idCompetition),
    Foreign key (licenceChefEquipe) references ORGANISATEUR(licenseOrganisateur)
);

create table TIREUR_EQUIPE(
    idEquipe int not null,
    licenceTireur int not null,
    primary key (idEquipe, licenceTireur),
    Foreign key (idEquipe) references EQUIPE(idEquipe),
    Foreign key (licenceTireur) references TIREUR(numeroLicenceTireur)
);

create table MATCH_EQUIPE(
    idMatchEquipe int not null auto_increment,
    idCompetition int not null,
    idEquipe1 int not null,
    scoreEquipe1 int not null,
    idEquipe2 int not null,
    scoreEquipe2 int not null,
    nbPhases int not null,
    primary key (idMatchEquipe),
    Foreign key (idEquipe1) references EQUIPE(idEquipe),
    Foreign key (idEquipe2) references EQUIPE(idEquipe)
);
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
-----------------------------Trigger------------------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------


-- select prenomTireur,numeroLicenceTireur, classement from TIREUR_DANS_COMPETITIONS natural join TIREUR natural join COMPETITION where idCompetition = 1 order by classement desc; Pour créer les poules au début



delimiter |
-- create or replace trigger verifDateInscription before insert on TIREUR_DANS_COMPETITIONS for each row
-- begin
--     declare dateDC date;
--     select dateDebutCompetiton into dateDC from COMPETITION where idCompetition = new.idCompetition;
--     if ( datediff(dateDC ,CURDATE()) <= 14  ) then
--         signal sqlstate '45000' set message_text = 'Les inscriptions pour cette compétitions sont close';
--     end if; 
-- end |


create or replace trigger verifDejaInserer before insert on TIREUR for each row 
begin
    declare numLc int;
    select numeroLicenceTireur into numLc from TIREUR where numeroLicenceTireur = new.numeroLicenceTireur;
    if (numLc = new.numeroLicenceTireur) then
        signal sqlstate '45000' set message_text = 'Ce numéro de licence est déjà dans la base';
    end if ;
end |

create or replace trigger estPasDejaAbitre before insert on TIREUR_DANS_COMPETITIONS for each row 
begin
    declare nbligne int;
    select count(*) into nbligne from ARBITRE_DANS_COMPETITIONS where numeroLicenceArbitre = new.numeroLicenceTireur and idCompetition = new.idCompetition;
    if (nbligne > 0) then
        signal sqlstate '45000' set message_text = 'Ce numéro de licence est déjà inscris en tant que Arbitre dans cette compétition';
    end if ;
end |

create or replace trigger estPasDejaTireur before insert on ARBITRE_DANS_COMPETITIONS for each row 
begin
    declare nbligne int;
    select count(*) into nbligne from TIREUR_DANS_COMPETITIONS where numeroLicenceTireur = new.numeroLicenceArbitre and idCompetition = new.idCompetition;
    if (nbligne > 0) then
        signal sqlstate '45000' set message_text = 'Ce numéro de licence est déjà inscris en tant que Tireur dans cette compétition';
    end if ;
end |

delimiter ; 