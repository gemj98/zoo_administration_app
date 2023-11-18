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

def get_ticket_id(cursor):
    get_ticket_id = """
    SELECT ticket_id FROM ticket;
    """
    cursor.execute(get_ticket_id)
    result = cursor.fetchall()
    return result

def check_visitor_ticket(cursor, ticket_id):
    check_visitor_ticket = """
    SELECT 
        CASE 
            WHEN COUNT(*) > 0 THEN 'Valid'
            ELSE 'Invalid'
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
    print(result)
    return result