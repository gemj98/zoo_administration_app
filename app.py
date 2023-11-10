import streamlit as st
import mysql.connector
import pandas as pd
from authenticator import Authenticator
from config import config as DBconfig
import queries.vet_queries as vet

import numpy as np

db = mysql.connector.connect(**DBconfig)
cursor = db.cursor()
userAuth = Authenticator(cursor)

if "isLogin" not in st.session_state:
    st.session_state.isLogin = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.emp_name = ""
    st.session_state.emp_ssn = ""


def create_database(cursor):
    """Create the 'userdb' database if it doesn't exist."""
    cursor.execute("CREATE DATABASE IF NOT EXISTS aaa")
    cursor.close()


def handle_log_in():
    (success, username, role, emp_name, emp_ssn) = userAuth.login(
        st.session_state.user_input, st.session_state.pswd_input
    )
    if success:
        st.session_state.isLogin = True
        st.session_state.username = username
        st.session_state.role = role
        st.session_state.emp_name = emp_name
        st.session_state.emp_ssn = emp_ssn


def handle_log_out():
    st.session_state.isLogin = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.emp_name = ""
    st.session_state.emp_ssn = ""


def handle_insert_animal_check(cursor, animal_id, health_status):
    vet.insert_animal_check(cursor, animal_id, health_status)
    db.commit()


def login_widget():
    username = st.text_input("Enter your username", key="user_input")
    password = st.text_input("Enter your password", key="pswd_input", type="password")
    loginButton = st.button("Login", on_click=handle_log_in)


def greetings():
    st.write(
        "Welcome back, {}. Your role is {}.".format(
            st.session_state.emp_name, st.session_state.role
        )
    )


def render_admin_options():
    menu = ["Home"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()


def render_vet_options():
    menu = [
        "Home",
        "Insert animal check",
        "Insert specie check",
        "Insert a prescription",
    ]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Insert animal check":
            # Select specie
            st.subheader("Insert animal check :turtle:")
            result = vet.get_species_single(cursor)
            species = dict(result)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options)

            # Select animal
            result = vet.get_animals_from_specie(cursor, species[specie.lower()])
            animals = dict(result)
            options = list(animals)
            animal = st.selectbox("Select an animal", animals)

            # List past 5 health checks
            result = vet.get_animal_checks_for_animal(cursor, animals[animal])
            df = pd.DataFrame(result, columns=["Record Date", "Health Status"])
            st.write("Health check history")
            st.dataframe(
                df,
                height=245,
                column_config={
                    "Health Status": st.column_config.CheckboxColumn(
                        help="Select your **favorite** widgets",
                        default=False,
                    )
                },
                use_container_width=True,
            )

            # Select health_status
            health_status = {"Healthy": 1, "Sick": 0}
            status = st.radio("Select health status", list(health_status))

            submit = st.button(
                "Insert animal check",
                on_click=lambda: handle_insert_animal_check(
                    cursor, animals[animal], health_status[status]
                ),
            )

        case "Insert specie check":
            st.write("Insert specie check")
        case "Insert a prescription":
            st.write("Insert a prescription")


def render_security_options():
    menu = ["Home"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()


def render_feeder_options():
    menu = ["Home"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()


def render_trainer_options():
    menu = ["Home"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()


def render_habitat_manager_options():
    menu = ["Home"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()


def render_visitor_options():
    st.write("Hello, visitor.")


def main():
    st.title("National Zoo System :elephant:")
    if not st.session_state.isLogin:
        login_widget()
    else:
        match st.session_state.role:
            case "admin":
                render_admin_options()
            case "veterinarian":
                render_vet_options()
            case "security":
                render_security_options()
            case "feeder":
                render_feeder_options()
            case "trainer":
                render_trainer_options()
            case "habitat_manager":
                render_habitat_manager_options()
            case _:
                render_visitor_options()
        logoutButton = st.sidebar.button("Logout", on_click=handle_log_out)


if __name__ == "__main__":
    main()
