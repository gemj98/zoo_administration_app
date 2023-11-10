from datetime import datetime
import streamlit as st
import mysql.connector
import pandas as pd
from config.db_config import config as DBconfig


def get_species_single(cursor):
    get_species_single_query = """
    SELECT common_name, specie_id FROM specie WHERE population IS null;
    """
    cursor.execute(get_species_single_query)
    result = cursor.fetchall()
    return result


def get_animals_from_specie(cursor, specie_id):
    get_species_single_query = """
    SELECT name, animal_id FROM animal WHERE specie_id=%s;
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
    cursor.execute(insert_animal_check_query, insert_animal_check_data)
