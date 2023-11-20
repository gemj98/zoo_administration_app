# SJSU CMPE 138 FALL 2023 TEAM10

DROP DATABASE IF EXISTS zoo;
CREATE database zoo;
USE zoo;

# -----  Employees and positions -------

CREATE TABLE employee (
    ssn CHAR(11) NOT NULL UNIQUE PRIMARY KEY,
    Ename VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL
);

# -------------  Tour & Tickets ----------------

CREATE TABLE tour(tour_id INT auto_increment PRIMARY KEY, Tname VARCHAR(30), max_cap INT, guide_ssn	 CHAR(11),
	FOREIGN KEY(guide_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL);


CREATE TABLE ticket(ticket_id INT auto_increment PRIMARY KEY, class varchar(30), start_date DATE NOT NULL, exp_date DATE NOT NULL, tour_id INT, 
	FOREIGN KEY(tour_id) references tour(tour_id) ON UPDATE CASCADE ON DELETE SET NULL);


#-----------   Habitat, Specie & Animals   -------------

CREATE TABLE habitat(habitat_id INT auto_increment PRIMARY KEY, Hname VARCHAR(30) NOT NULL UNIQUE,
	area REAL, population REAL, temperature REAL, manager_ssn CHAR(11), 
	FOREIGN KEY(manager_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL);

CREATE TABLE specie (specie_id INT auto_increment PRIMARY KEY, common_name VARCHAR(50) NOT NULL UNIQUE, population INT,
	 diet VARCHAR(120), life_expectancy INT, avg_weight REAL, avg_size REAL, habitat_id INT,
	 FOREIGN KEY(habitat_id) references habitat(habitat_id) ON UPDATE CASCADE ON DELETE SET NULL);

CREATE TABLE animal (animal_id INT auto_increment PRIMARY KEY, Aname VARCHAR(30) NOT NULL UNIQUE, 
	weight REAL, size REAL, health_status BOOLEAN, specie_id INT NOT NULL, 
    trainer_ssn CHAR(11), training_status BOOLEAN, 
    FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE RESTRICT, 
    FOREIGN KEY(trainer_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL);


#  ----------  Actions with habitats, species or animals ----------------
 
CREATE TABLE tour_sees(tour_id INT, habitat_id INT, 
	PRIMARY KEY (tour_id, habitat_id),
	FOREIGN KEY(tour_id) references tour(tour_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(habitat_id) references habitat(habitat_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE meal_records(feeder_ssn CHAR(11), specie_id INT, record_date TIMESTAMP, 
	PRIMARY KEY(specie_id, record_date), 
	FOREIGN KEY(feeder_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL, 
	FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE animal_status(status_id INT, status_name varchar(30));

CREATE TABLE specie_check(vet_ssn CHAR(11), specie_id INT, record_date TIMESTAMP, health_status varchar(300), 
	PRIMARY KEY(specie_id, record_date), 
	FOREIGN KEY(vet_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL, 
	FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE animal_check(
    vet_ssn CHAR(11),
    animal_id INT, 
    record_date TIMESTAMP,
    health_status BOOLEAN,
    FOREIGN KEY (vet_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (animal_id) REFERENCES animal(animal_id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (animal_id, record_date)
);

DELIMITER //
CREATE TRIGGER trig_animalCheckInsert
AFTER INSERT ON animal_check
FOR EACH ROW
BEGIN
	UPDATE animal
	SET health_status = NEW.health_status
	WHERE animal.animal_id = NEW.animal_id;
END;
//
DELIMITER ;
              
# ----------  Tables for Veterinatian -----------------
              
CREATE TABLE drug (drug_id INT auto_increment PRIMARY KEY, Dname VARCHAR(45), ingredients VARCHAR(200));

CREATE TABLE prescription (drug_id INT NOT NULL, animal_id INT NOT NULL, vet_ssn CHAR(11) NOT NULL, start_date DATE NOT NULL, end_date DATE, dose VARCHAR(300) NOT NULL,
                           PRIMARY KEY(drug_id, animal_id, start_date),
                           FOREIGN KEY(drug_id) references drug(drug_id) ON UPDATE CASCADE ON DELETE RESTRICT,
                           FOREIGN KEY(vet_ssn) references employee(ssn),
                           FOREIGN KEY(animal_id) references animal(animal_id) ON UPDATE CASCADE ON DELETE RESTRICT);


# ---------------   Table for user login -----------------

CREATE TABLE user (username VARCHAR(30) NOT NULL PRIMARY KEY, password VARCHAR(60) NOT NULL, ssn CHAR(11),
    FOREIGN KEY(ssn) references employee(ssn));


# -/-/-/-/-/-/--/-/-/-/-/-/ Populate tables /-/-/-/-/-/-/-/-/-/-/-/-/-/

-- CREATE TABLE habitat(habitat_id INT auto_increment PRIMARY KEY, name VARCHAR(30) NOT NULL UNIQUE,
-- 	area REAL, population REAL, temperature REAL, manager_ssn CHAR(11), 
-- 	FOREIGN KEY(manager_ssn) references employee(ssn) ON UPDATE CASCADE ON DELETE SET NULL);
  
INSERT INTO employee (ssn, Ename, position) values
	('867-43-6911', 'Helaine Anderson', 'trainer'),
	('622-72-0793', 'Jereme Smith', 'trainer'),
	('628-43-7850', 'Pablo Williams', 'habitat_manager'),
	('362-78-0387', 'Idelle Johnson', 'habitat_manager'),
	('535-08-5848', 'Davidson Wilson', 'veterinarian'),
	('514-24-9839', 'Ophelia Miller', 'feeder'),
	('377-24-8838', 'Glen Garcia', 'security'),
	('593-63-0610', 'Forrester Evans', 'tour_guide'),
	('761-60-4472', 'Sibelle Collins', 'admin'),
    ('456-21-9872', 'John Doe', 'tour_guide');
    
/*
	('683-66-8443', 'Meaghan Dunphie', 'veterinarian'),
	('835-52-2763', 'Giorgia Longstreeth', 'security'),
	('478-65-2874', 'Nancee Giamelli', 'trainer'),
	('870-73-3106', 'Opaline Balnaves', 'feeder'),
	('551-76-5116', 'Conny Druce', 'veterinarian'),
	('697-84-7388', 'Clarice Loidl', 'trainer');
*/
  
INSERT INTO habitat (Hname, area, temperature, manager_ssn) values 
	('carivores', 195.4, 64, '628-43-7850'),
	('herbivores', 250.7, 64, '628-43-7850'),
    ('reptiles', 80.7, 75, '362-78-0387'),
    ('aquarium', 62.4, 78, '362-78-0387');

# weight in lbs, height in inch.
insert into specie (common_name, population, diet, life_expectancy, avg_weight, avg_size, habitat_id)
values ('lion', null, 'ground beef, beef femur', 15, 420, 44.4, 1),
	('elephant', null, 'hay, fruits, vegetables', 40, 7000, 134.4, 2),
	('giraffe', null, 'acacia and mimosa leaves', 23, 4000, 183.6, 2),
	('zebra', null, 'hay, alfalfa, carrots', 30,  750, 50.4, 2),
    ('pancake tortoise', null, 'collard greens, kale, carrots', 25, 1.5, 6.5, 3),
    ('banded iguana', null, 'leaves, fruit, and flowers of trees and shrubs', 12, 0.44, 21, 3),
    ('goldfish', 22, 'food pellets, algae wafers, brine shrimp', 12, 0.84, 4.5, 4),
    ('neon tetra', 15, 'food pellets, algae wafers, brine shrimp', 10, 0.23, 1.5, 4);

INSERT INTO animal(specie_id, Aname, weight, size, health_status, trainer_ssn, training_status) values
# lions
	(1, 'Simba', 451, 46.7, 1, '867-43-6911', 0),
	(1, 'Zira', 405, 40.1, 0, null, -1),
	(1, 'Tina', 405, 40.1, 0, '867-43-6911', 1),
# elephants
    (2, 'Abigail', 6502, 124.7, 0, '622-72-0793', 1),
    (2, 'Clover', 7012, 135.2, 0, null, -1),
# giraffe
	(3, 'Cleopatra', 3954, 164.5, 0, null, -1),
# zebra
	(4, 'Daffodil', 760, 52.1, 1, null, -1),
    (4, 'Emma', 745, 50.7, 0, null, -1),
# tortoise
	(5, 'Indigo', 1.1, 4.8, 0, null, -1),
	(5, 'Karma', 1.6, 5.4, 0, null, -1),
	(5, 'Daisy', 1.4, 5.1, 0, null, -1),
#banded iguana
	(6, 'Luna', 0.4, 15, 0, null, -1),
	(6, 'Jasmine', 0.5, 23, 0, null, -1);

INSERT INTO drug(Dname, ingredients) values
	('NexGard Chew', '136 mg Afoxolaner'),
	('Aqua-Mox Forte', '500 mg Amoxicillin'),
	('Acepromazine', 'Each mL contains: acepromazine maleate 10 mg, sodium citrate 0.36%, citric acid 0.075%, benzyl alcohol 1% and water for injection');


INSERT INTO animal_status(status_id, status_name) values(-1, "Untrained");
INSERT INTO animal_status(status_id, status_name) values(0, "In Progress");
INSERT INTO animal_status(status_id, status_name) values(1, "Complete");

INSERT INTO prescription(drug_id, animal_id, vet_ssn, start_date, end_date, dose) values
	(1, 1, '535-08-5848', '2023-10-12', '2023-11-25', 'One each morning'),
	(2, 1, '535-08-5848', '2023-10-14', '2023-11-30', 'Two each morning'),
	(3, 1, '535-08-5848', '2023-10-13', '2023-10-30', 'Two each morning'),
	(3, 2, '535-08-5848', '2023-10-18', '2023-11-12', 'Three each morning'),
	(3, 3, '535-08-5848', '2023-10-06', '2023-11-18', 'Four each morning');

INSERT INTO tour(Tname, max_cap, guide_ssn) values
	('Meet carnivores', 20, '593-63-0610'),
	('Meet herbivores', 40, '456-21-9872'),
	('Meet reptiles', 30, '593-63-0610'),
    ('Meet aquatic', 70, '456-21-9872');

INSERT INTO tour(tour_id, Tname, max_cap, guide_ssn) values
    (-1, 'COMPLETE', 0, '761-60-4472');
    
INSERT INTO ticket(class, start_date, exp_date, tour_id) values
	('General', '2023-11-15', '2023-11-18', 1),
	('VIP', '2023-11-15', '2023-11-20', 1),
	('First', '2023-11-17', '2023-12-15', 3),
    ('General', '2023-11-15', '2023-12-15', 4),
	('VIP', '2023-11-16', '2023-12-15', 3),
	('First', '2023-11-16', '2023-12-15', 2),
    ('General', '2023-11-16', '2023-12-15', 1),
	('VIP', '2023-11-12', '2023-12-15', 2),
	('First', '2023-11-16', '2023-12-15', 3),
    ('General', '2023-11-15', '2023-12-15', 4),
	('VIP', '2023-11-16', '2023-12-15', 4),
	('First', '2023-11-18', '2023-12-15', 3),
    ('General', '2023-11-19', '2023-12-15', 4);
	
INSERT INTO tour_sees(tour_id, habitat_id) values
	(1, 1),
	(2, 2),
    (3, 3),
    (4, 4);
