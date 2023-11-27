# SJSU CMPE 138 FALL 2023 TEAM10

from datetime import datetime
import streamlit as st
import mysql.connector
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s {%(name)s} [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler = logging.FileHandler("Log/app_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_species(cursor):
    get_species_query = """
    SELECT common_name, specie_id FROM specie;
    """
    cursor.execute(get_species_query)
    result = cursor.fetchall()
    return result


def insert_meal_record(cursor, specie_id):
    insert_meal_record_query = """
    INSERT INTO meal_records(feeder_ssn, specie_id, record_date) values(%s, %s, CURRENT_TIMESTAMP());
    """
    try:
        cursor.execute(insert_meal_record_query, [st.session_state.emp_ssn, specie_id])
    except mysql.connector.Error as err:
        logger.error(
            "Inserting meal record for specie_id={}: {}".format(specie_id, err.msg)
        )
        return err.msg
    else:
        logger.info("Inserting meal record for specie_id={}: Success".format(specie_id))
        return ""


def get_meal_records(cursor, specie_id):
    get_meal_records_query = """
    SELECT record_date FROM meal_records where specie_id=%s ORDER BY record_date DESC;
    """
    cursor.execute(get_meal_records_query, [specie_id])
    result = cursor.fetchall()
    return result


def get_status_options(cursor):
    get_status_options_query = """
    SELECT status_name, status_id FROM animal_status;
    """
    cursor.execute(get_status_options_query)
    result = cursor.fetchall()
    return result


def get_animals_from_specie(cursor, specie_id):
    get_species_single_query = """
    SELECT Aname, animal_id FROM animal WHERE specie_id=%s;
    """
    cursor.execute(get_species_single_query, [specie_id])
    result = cursor.fetchall()
    return result


def get_animal_status(cursor, animal_id):
    get_animal_status_query = """
    SELECT status_name FROM animal_status WHERE status_id IN (SELECT training_status FROM animal WHERE animal_id = %s);
    """
    cursor.execute(get_animal_status_query, [animal_id])
    result = cursor.fetchall()
    return result


def update_animal_status(cursor, animal_id, status_id):
    try:
        if status_id >= 0:
            update_animal_status_query = """
            UPDATE animal SET training_status = %s, trainer_ssn = %s WHERE animal_id = %s;
            """
            cursor.execute(
                update_animal_status_query,
                [status_id, st.session_state.emp_ssn, animal_id],
            )
        else:
            update_animal_status_query = """
            UPDATE animal SET training_status = %s, trainer_ssn = NULL WHERE animal_id = %s;
            """
            cursor.execute(update_animal_status_query, [status_id, animal_id])
    except mysql.connector.Error as err:
        logger.error(
            "Updating training status for animal_id={}: {}".format(animal_id, err.msg)
        )
        return err.msg
    else:
        logger.info(
            "Updating training status for animal_id={}: Success".format(animal_id)
        )
        return ""


def get_habitat(cursor):
    get_habitat_query = """
    SELECT Hname, habitat_id FROM habitat;
    """
    cursor.execute(get_habitat_query)
    result = cursor.fetchall()
    return result


def get_habitat_temp(cursor, habitat_id):
    get_habitat_temp_query = """
    SELECT temperature FROM habitat WHERE habitat_id = %s;
    """
    cursor.execute(get_habitat_temp_query, [habitat_id])
    result = cursor.fetchall()
    return result


def update_habitat_temp(cursor, habitat_id, temp):
    update_habitat_temp_query = """
    UPDATE habitat SET temperature = %s WHERE habitat_id = %s
    """
    try:
        cursor.execute(update_habitat_temp_query, [temp, habitat_id])
    except mysql.connector.Error as err:
        logger.error(
            "Updating habitat temperature for habitat_id={}: {}".format(
                habitat_id, err.msg
            )
        )
        return err.msg
    else:
        logger.info(
            "Updating habitat temperature for habitat_id={}: Success".format(habitat_id)
        )
        return ""
