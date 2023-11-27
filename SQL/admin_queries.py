# SJSU CMPE 138 FALL 2023 TEAM10

from datetime import datetime
import pandas as pd
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


def run_query(db, sql_query):
    result = ""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_query)
            values = cursor.fetchall()
            columns = cursor.column_names
            print(columns)
            if len(columns) != 0:
                result = pd.DataFrame(values, columns=columns)

    except mysql.connector.Error as err:
        logger.exception("Running custom query: {}".format(err))
        return (result, err)
    else:
        logger.info("Running custom query: Success")
        return (result, "")
