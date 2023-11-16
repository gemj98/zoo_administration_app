from datetime import datetime
import streamlit as st
import pandas as pd
from config import config as DBconfig


def add_new_tour(cursor, tour_name, max_cap, habitat_id):
    add_new_tour = """
    INSERT INTO tour (name, max_cap, guide_ssn) VALUES (%s, %s,%s);
    """
    insert_tour_data = (
        tour_name,
        max_cap,
        st.session_state.emp_ssn,
    )
    cursor.execute(add_new_tour, insert_tour_data)
    add_tour_sees = """
	INSERT INTO tour_sees (tour_id, habitat_id) VALUES (LAST_INSERT_ID(), %s);
	"""
    cursor.execute(add_tour_sees, [habitat_id])

def modify_tour(cursor, tour_id, tour_name, max_cap):
    modify_tour = """
    UPDATE tour
    SET name = %s, max_cap = %s
    WHERE tour_id = %s AND guide_ssn = %s;
    """
    tour_data = (
        tour_name,
        max_cap,
        tour_id,
        st.session_state.emp_ssn,
    )
    cursor.execute(modify_tour, tour_data)

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
    cursor.execute(modify_tour_sees, tour_sees_data)

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

    nullify_ticket = """
    UPDATE ticket
    SET tour_id = NULL
    WHERE tour_id = %s;
    """
    result_ticket = cursor.execute(nullify_ticket, [tour_id])
    return result_tour