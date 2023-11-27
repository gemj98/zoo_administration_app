# SJSU CMPE 138 FALL 2023 TEAM10


USE zoo;

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
             