SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `Escrime` DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci;
USE `Escrime`;
-- not null auto_increment 


create table LIEU(
    idLieu int not null auto_increment,
    adresse varchar(100) not null,
    region varchar(50) not null,
    department varchar(50) not null,
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
    idOrganisateur int not null auto_increment,
    nomOrganisateur varchar(50) not null,
    prenomOrganisateur varchar(50) not null,
    licenseOrganisateur varchar(50) not null,
    primary key (idOrganisateur)
);

create table ORGANISATEURDANSCLUB(
    idClub int not null,
    idOrganisateur int not null,
    primary key (idClub, idOrganisateur),
    Foreign key(idCLub) references CLUB(idCLub),
    Foreign key(idOrganisateur) references ORGANISATEUR(idOrganisateur)
);

create table TIREUR(
    idTireur int not null auto_increment,
    nomTireur varchar(50) not null,
    prenomTireur varchar(50) not null,
    numeroLicenceTireur varchar(10) not null,
    classement Float(10,2) not null,
    idSexeTireur int not null,
    primary key (idTireur),
    Foreign key(idSexeTireur) references SEXE(idSexe)
);

create table ARBITRE(
    idArbitre int not null auto_increment,
    nomArbitre varchar(30) not null,
    prenomArbitre varchar(30) not null,
    numeroLicenceArbitre varchar(10) not null,
    primary key (idArbitre)
);

create table COMPETITION(
    idCompetition int not null auto_increment,
    intituleCompet varchar(42) not null,
    saison varchar(20) not null,
    estFinie boolean not null,
    coefficientCompetition Float(10,2) not null,
    classementFinal varchar(100), -- En faire une fonction plus tard 
    arbresMatchs varchar(100), -- En faire une fonction plus tard 
    dateDebutCompetiton date not null,
    idLieuCompetition int not null,
    idCategorieCompetition int not null,
    idSexeCompetition int not null,
    idArmeCompetition int not null,
    primary key (idCompetition),
    Foreign key(idLieuCompetition) references LIEU(idLieu),
    Foreign key(idCategorieCompetition) references CATEGORIE(idCategorie),
    Foreign key(idSexeCompetition) references SEXE(idSexe),
    Foreign key(idArmeCompetition) references ARME(idArme)
);

create table MATCHELIMINATION(
    idMatchElimination int not null auto_increment,
    nomMatchElimination varchar(60),
    nbPhases int not null,
    numeroPiste int not null,
    primary key (idMatchElimination)
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
    nbPhases int not null,
    idPoule int not null,
    primary key(idMatchPoule),
    Foreign key(idPoule) references POULE(idPoule)
);

create table TIREUR_DANS_COMPETITIONS(
    idTireur int not null,
    idCompetition int not null,
    primary key (idTireur, idCompetition),
    Foreign key(idTireur) references TIREUR(idTireur),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table TIREUR_DANS_POULE(
    idTireur int not null,
    idPoule int not null,
    primary key (idTireur, idPoule),
    Foreign key(idTireur) references TIREUR(idTireur),
    Foreign key(idPoule) references POULE(idPoule)
);

create table ARBITRE_DANS_COMPETITIONS(
    idArbitre int not null,
    idCompetition int not null,
    primary key (idArbitre, idCompetition),
    Foreign key(idArbitre) references ARBITRE(idArbitre),
    Foreign key(idCompetition) references COMPETITION(idCompetition)
);

create table ARBITRE_POULE(
    idArbitre int not null,
    idPoule int not null,
    primary key (idArbitre, idPoule),
    Foreign key(idArbitre) references ARBITRE(idArbitre),
    Foreign key(idPoule) references POULE(idPoule)
);

create table ARBITRE_ELIMINATION(
    idArbitre int not null,
    idMatchElimination int not null,
    primary key (idArbitre, idMatchElimination),
    Foreign key(idArbitre) references ARBITRE(idArbitre),
    Foreign key(idMatchElimination) references MATCHELIMINATION(idMatchElimination)
);