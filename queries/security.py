from datetime import datetime
import streamlit as st
import pandas as pd
from config import config as DBconfig


def check_visitor_ticket(cursor, ticket_id):
    check_visitor_ticket = """
    SELECT 
        CASE 
            WHEN COUNT(*) > 0 THEN 'Ticket Found and Valid'
            ELSE 'No Ticket Found or Invalid Details'
        END as Status
    FROM 
        ticket
    WHERE 
        ticket_id = %s AND
        start_date <= CURRENT_DATE AND
        exp_date >= CURRENT_DATE;
    """
    cursor.execute(check_visitor_ticket, [ticket_id])
    result = cursor.fetchall()
    return result