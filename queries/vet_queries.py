from datetime import datetime
import streamlit as st
import mysql.connector
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s {%(name)s} [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler = logging.FileHandler("app_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_species_single(cursor):
    get_species_single_query = """
    SELECT common_name, specie_id FROM specie WHERE population IS null;
    """
    cursor.execute(get_species_single_query)
    result = cursor.fetchall()
    return result


def get_species_multiple(cursor):
    get_species_single_query = """
    SELECT common_name, specie_id FROM specie WHERE population IS NOT null;
    """
    cursor.execute(get_species_single_query)
    result = cursor.fetchall()
    return result


def get_animals_from_specie(cursor, specie_id):
    get_species_single_query = """
    SELECT Aname, animal_id FROM animal WHERE specie_id=%s;
    """
    cursor.execute(get_species_single_query, [specie_id])
    result = cursor.fetchall()
    return result


def get_animal_checks_for_animal(cursor, animal_id):
    animal_checks_for_animal_query = """
    SELECT record_date, health_status FROM animal_check WHERE animal_id=%s
    ORDER BY record_date DESC;
    """
    cursor.execute(animal_checks_for_animal_query, [animal_id])
    result = cursor.fetchall()
    return result


def get_prescriptions_for_animal(cursor, animal_id):
    prescriptions_query = """
    SELECT NOW() < end_date AS isActive, 
           Dname, dose, start_date, end_date, Ename
    FROM (((prescription NATURAL JOIN drug) NATURAL JOIN animal)
    JOIN employee ON vet_ssn = ssn)
    WHERE animal_id=%s
    ORDER BY end_date DESC;
    """
    cursor.execute(prescriptions_query, [animal_id])
    result = cursor.fetchall()
    return result


def get_drugs(cursor):
    drugs_query = """
    SELECT Dname, drug_id FROM drug;
    """
    cursor.execute(drugs_query)
    result = cursor.fetchall()
    return result


def insert_animal_check(cursor, animal_id, health_status):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_animal_check_query = """
    INSERT INTO animal_check(vet_ssn, animal_id, record_date, health_status) values
	(%s, %s, %s, %s);
    """
    insert_animal_check_data = (
        st.session_state.emp_ssn,
        animal_id,
        current_date,
        health_status,
    )
    try:
        cursor.execute(insert_animal_check_query, insert_animal_check_data)
    except mysql.connector.Error as err:
        logger.error(
            "Inserting animal check for animal_id={}: {}".format(animal_id, err.msg)
        )
        return err.msg
    else:
        logger.info(
            "Inserting animal check for animal_id={}: Success".format(animal_id)
        )
        return ""


def get_specie_checks_for_specie(cursor, specie_id):
    specie_checks_for_specie_query = """
    SELECT record_date, health_status FROM specie_check WHERE specie_id=%s
    ORDER BY record_date DESC;
    """
    cursor.execute(specie_checks_for_specie_query, [specie_id])
    result = cursor.fetchall()
    return result


def insert_specie_check(cursor, specie_id, health_status):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_specie_check_query = """
    INSERT INTO specie_check(vet_ssn, specie_id, record_date, health_status) values
	(%s, %s, %s, %s);
    """
    insert_specie_check_data = (
        st.session_state.emp_ssn,
        specie_id,
        current_date,
        health_status,
    )
    try:
        cursor.execute(insert_specie_check_query, insert_specie_check_data)
    except mysql.connector.Error as err:
        logger.error(
            "Inserting specie check for specie_id={}: {}".format(specie_id, err.msg)
        )
        return err.msg
    else:
        logger.info(
            "Inserting specie check for specie_id={}: Success".format(specie_id)
        )
        return ""


def insert_prescription(cursor, drug_id, animal_id, end_date, dose):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_prescription_query = """
    INSERT INTO prescription(drug_id, animal_id, vet_ssn,
                             start_date, end_date, dose) values
	(%s, %s, %s, %s, %s, %s);
    """
    insert_prescription_data = (
        drug_id,
        animal_id,
        st.session_state.emp_ssn,
        current_date,
        end_date,
        dose,
    )
    try:
        cursor.execute(insert_prescription_query, insert_prescription_data)
    except mysql.connector.Error as err:
        logger.error(
            "Inserting prescription for animal_id={}: {}".format(animal_id, err.msg)
        )
        return err.msg
    else:
        logger.info(
            "Inserting prescription for animal_id={}: Success".format(animal_id)
        )
        return ""
