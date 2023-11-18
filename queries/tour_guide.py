# SJSU CMPE 138 FALL 2023 TEAM10

from datetime import datetime
import streamlit as st
import mysql.connector
from config import config as DBconfig
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

def get_habitat_id(cursor):
    get_habitat_id = """
    SELECT habitat_id FROM habitat;
    """
    cursor.execute(get_habitat_id)
    result = cursor.fetchall()
    return result

def get_tour_id(cursor):
    get_tour_id = """
    SELECT tour_id FROM tour WHERE guide_ssn = %s;
    """
    cursor.execute(get_tour_id, [st.session_state.emp_ssn])
    result = cursor.fetchall()
    return result

def add_new_tour(cursor, tour_name, max_cap, habitat_id):
    
    add_new_tour = """
    INSERT INTO tour (Tname, max_cap, guide_ssn) VALUES (%s,%s,%s);
    """
    insert_tour_data = (
        tour_name,
        max_cap,
        st.session_state.emp_ssn,
    )
    add_tour_sees = """
	INSERT INTO tour_sees (tour_id, habitat_id) VALUES (LAST_INSERT_ID(), %s);
	"""
    try:
        cursor.execute(add_new_tour, insert_tour_data)
        cursor.execute(add_tour_sees, (habitat_id))
    except mysql.connector.Error as err:
        logger.error(
            "Inserting tour for tour_name={} and habitat_id={}: {}".format(tour_name, habitat_id, err.msg)
        )
        return (err.msg, "")
    else:
        logger.info(
            "Inserting tour for tour_name={}: Success".format(tour_name)
        )
        return ("", "Successfully added")

def modify_tour(cursor, tour_id, tour_name, max_cap):
    modify_tour = """
    UPDATE tour
    SET Tname = %s, max_cap = %s
    WHERE tour_id = %s AND guide_ssn = %s;
    """
    tour_data = (
        tour_name,
        max_cap,
        tour_id,
        st.session_state.emp_ssn
    )
    try:
        logger.info(
            "Modify tour for tour_id={}, tour_name={}, max_cap={}, ssn={}: Try".format(tour_id, tour_name, max_cap, st.session_state.emp_ssn)
        )
        cursor.execute(modify_tour, [tour_name, max_cap, tour_id, st.session_state.emp_ssn])
    except mysql.connector.Error as err:
        logger.error(
            "Modify tour for tour_id={}: {}".format(tour_id, err.msg)
        )
        st.session_state.error = err.msg
    else:
        logger.info(
            "Modify tour for tour_id={}: Success".format(tour_id)
        )
        st.session_state.error = "Success"
    

def modify_tour_sees(cursor, tour_id, habitat_id):
    modify_tour_sees = """
    UPDATE tour_sees
    SET habitat_id = %s
    WHERE tour_id = %s;
    """
    tour_sees_data = (
        habitat_id,
        tour_id,
    )
    try:
        cursor.execute(modify_tour_sees, tour_sees_data)
    except mysql.connector.Error as err:
        logger.error(
            "Modify tour_sees for tour_id={}: {}".format(tour_id, err.msg)
        )
        st.session_state.error = err.msg
    else:
        logger.info(
            "Modify tour_sees for tour_id={}: Success".format(tour_id)
        )
        st.session_state.error = "Success"
    

def provide_tour(cursor, tour_id):
    tour_guide_provide_tour = """
    SELECT ticket.ticket_id, ticket.class
    FROM ticket, tour
    WHERE ticket.tour_id = %s AND tour.guide_ssn = %s
    """
    tour_guide_ticket_data = (
        tour_id,
        st.session_state.emp_ssn,
    )
    result_tour = cursor.execute(tour_guide_provide_tour, tour_guide_ticket_data)
    result_tour = cursor.fetchall()

    nullify_ticket = """
    UPDATE ticket
    SET tour_id = NULL
    WHERE tour_id = %s;
    """
    try:
        cursor.execute(nullify_ticket, [tour_id])
    except mysql.connector.Error as err:
        logger.error(
            "Provide tour for tour_id={}: {}".format(tour_id, err.msg)
        )
        return ("", err.msg)
    else:
        logger.info(
            "Provide tour for tour_id={}: Success".format(tour_id)
        )
        return (result_tour, "")