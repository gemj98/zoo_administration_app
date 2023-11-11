DROP database zoo;
CREATE database zoo;
USE zoo;

# -----  Employees and positions -------

CREATE TABLE employee (
    ssn CHAR(9) NOT NULL UNIQUE PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL
);

CREATE TABLE trainer (
    employee_ssn CHAR(9) NOT NULL PRIMARY KEY,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE feeder (
    employee_ssn CHAR(9) NOT NULL PRIMARY KEY,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE habitat_manager (
    employee_ssn CHAR(9) NOT NULL PRIMARY KEY,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE tour_guide (
    employee_ssn CHAR(9) NOT NULL PRIMARY KEY, tour_id INT,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE veterinarian (
    employee_ssn CHAR(9) NOT NULL PRIMARY KEY,
    years_of_experience INT,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn) ON UPDATE CASCADE ON DELETE CASCADE
);

# -------------  Tour & Tickets ----------------

CREATE TABLE tour(tour_id INT auto_increment PRIMARY KEY, name VARCHAR(30), max_cap INT, guide_ssn char(9),
	FOREIGN KEY(guide_ssn) references tour_guide(employee_ssn) ON UPDATE CASCADE ON DELETE SET NULL);


CREATE TABLE ticket(ticket_id INT auto_increment PRIMARY KEY, class varchar(30), start_date DATE NOT NULL, exp_date DATE NOT NULL, tour_id INT, 
	FOREIGN KEY(tour_id) references tour(tour_id) ON UPDATE CASCADE ON DELETE SET NULL);


#-----------   Habitat, Specie & Animals   -------------

CREATE TABLE habitat(habitat_id INT auto_increment PRIMARY KEY, name VARCHAR(30) NOT NULL UNIQUE,
	area REAL, population REAL, temperature REAL, manager_ssn char(9), 
	FOREIGN KEY(manager_ssn) references habitat_manager(employee_ssn) ON UPDATE CASCADE ON DELETE SET NULL);

CREATE TABLE specie (specie_id INT auto_increment PRIMARY KEY, common_name VARCHAR(50) NOT NULL UNIQUE, population INT,
	 diet VARCHAR(120), life_expectancy INT, avg_weight REAL, avg_size REAL, habitat_id INT,
	 FOREIGN KEY(habitat_id) references habitat(habitat_id) ON UPDATE CASCADE ON DELETE SET NULL);

CREATE TABLE animal (animal_id INT auto_increment PRIMARY KEY, Name VARCHAR(30) NOT NULL UNIQUE, 
	weight REAL, size REAL, healthy BOOLEAN, specie_id INT NOT NULL, 
    trainer_ssn char(9), training_status varchar(30), 
    FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE RESTRICT, 
    FOREIGN KEY(trainer_ssn) references trainer(employee_ssn) ON UPDATE CASCADE ON DELETE SET NULL);


#  ----------  Actions with habitats, species or animals ----------------
 
CREATE TABLE tour_sees(tour_id INT, habitat_id INT, 
	PRIMARY KEY (tour_id, habitat_id),
	FOREIGN KEY(tour_id) references tour(tour_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(habitat_id) references habitat(habitat_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE meal_records(feeder_ssn char(9), specie_id INT, record_date TIMESTAMP, 
	PRIMARY KEY(specie_id, record_date), 
	FOREIGN KEY(feeder_ssn) references feeder(employee_ssn) ON UPDATE CASCADE ON DELETE SET NULL, 
	FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE species_check(vet_ssn char(9), specie_id INT, record_date TIMESTAMP, health_status varchar(30), 
	PRIMARY KEY(specie_id, record_date), 
	FOREIGN KEY(vet_ssn) references veterinarian(employee_ssn) ON UPDATE CASCADE ON DELETE SET NULL, 
	FOREIGN KEY(specie_id) references specie(specie_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE animal_check(
    vet_ssn CHAR(9),
    animal_id INT, 
    record_date DATE,
    health_status varchar(30),
    FOREIGN KEY (vet_ssn) REFERENCES veterinarian(employee_ssn) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (animal_id) REFERENCES animal(animal_id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (vet_ssn, animal_id, record_date)
);
              
# ----------  Tables for Veterinatian -----------------
              
CREATE TABLE drug (drug_id INT auto_increment PRIMARY KEY, name VARCHAR(45), ingredients VARCHAR(200));

CREATE TABLE prescription (drug_id INT NOT NULL, animal_id INT NOT NULL, vet_ssn CHAR(9) NOT NULL, start_date DATE NOT NULL, end_date DATE, dose VARCHAR(300) NOT NULL,
                           PRIMARY KEY(drug_id, animal_id, start_date),
                           FOREIGN KEY(drug_id) references drug(drug_id) ON UPDATE CASCADE ON DELETE RESTRICT,
                           FOREIGN KEY(vet_ssn) references veterinarian(employee_ssn),
                           FOREIGN KEY(animal_id) references animal(animal_id) ON UPDATE CASCADE ON DELETE RESTRICT);


# ---------------   Table for user login -----------------

CREATE TABLE user (username VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY, password VARCHAR(60) NOT NULL, ssn CHAR(9) UNIQUE,
    FOREIGN KEY(ssn) references employee(ssn));

#INSERT INTO user(username, password) VALUES ("a","A"), ("b", "B"), ("c", "C");