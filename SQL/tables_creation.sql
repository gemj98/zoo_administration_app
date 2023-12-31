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

CREATE TABLE tour(tour_id INT auto_increment PRIMARY KEY, Tname VARCHAR(30) NOT NULL UNIQUE, max_cap INT, guide_ssn	 CHAR(11),
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

CREATE TABLE animal_status(status_id INT PRIMARY KEY, status_name varchar(30) NOT NULL);

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


