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
error = ""

if "isLogin" not in st.session_state:
    st.session_state.isLogin = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.emp_name = ""
    st.session_state.emp_ssn = ""
    st.session_state.error = ""


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
    userAuth.logout()
    st.session_state.isLogin = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.emp_name = ""
    st.session_state.emp_ssn = ""


def handle_insert_animal_check(cursor, animal_id, health_status):
    st.session_state.error = vet.insert_animal_check(cursor, animal_id, health_status)
    db.commit()


def handle_insert_specie_check(cursor, specie_id, health_status):
    st.session_state.error = vet.insert_specie_check(cursor, specie_id, health_status)
    db.commit()


def handle_insert_prescription(cursor, drug_id, animal_id, end_date, dose):
    st.session_state.error = vet.insert_prescription(
        cursor, drug_id, animal_id, end_date, dose
    )
    db.commit()


def clear_error():
    st.session_state.error = ""


def login_widget():
    with st.form("login_form"):
        username = st.text_input("Enter your username", key="user_input")
        password = st.text_input(
            "Enter your password", key="pswd_input", type="password"
        )
        loginButton = st.form_submit_button("Login", on_click=handle_log_in)


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
            st.subheader("Insert animal check :turtle:")

            # Select specie
            result = vet.get_species_single(cursor)
            species = dict(result)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options).lower()

            # Select animal
            result = vet.get_animals_from_specie(cursor, species[specie])
            print(result)
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

            with st.form("animal_check_form"):
                # Select health_status
                health_status = {"Healthy": 1, "Sick": 0}
                status = st.radio(
                    "Select health status", list(health_status), key="animal_status"
                )

                submit = st.form_submit_button(
                    "Insert animal check",
                    on_click=lambda: handle_insert_animal_check(
                        cursor,
                        animal_id=animals[animal],
                        health_status=health_status[st.session_state.animal_status],
                    ),
                )

        case "Insert specie check":
            st.subheader("Insert specie check :fish:")

            # Select specie
            result = vet.get_species_multiple(cursor)
            species = dict(result)
            print(species)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options).lower()

            # List past 5 health checks
            result = vet.get_specie_checks_for_specie(cursor, species[specie])
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

            with st.form("animal_check_form"):
                # Select health_status
                health_status = {"Healthy": 1, "Sick": 0}
                status = st.radio(
                    "Select health status", list(health_status), key="specie_status"
                )

                submit = st.form_submit_button(
                    "Insert specie check",
                    on_click=lambda: handle_insert_specie_check(
                        cursor,
                        specie_id=species[specie],
                        health_status=health_status[st.session_state.specie_status],
                    ),
                )
        case "Insert a prescription":
            st.subheader("Create a prescription 💊")

            # Select specie
            result = vet.get_species_single(cursor)
            species = dict(result)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options).lower()

            # Select animal
            result = vet.get_animals_from_specie(cursor, species[specie])
            animals = dict(result)
            # options = list(animals)
            animal = st.selectbox("Select an animal", animals)

            # List past 5 health checks
            result = vet.get_prescriptions_for_animal(cursor, animals[animal])
            df = pd.DataFrame(
                result,
                columns=[
                    "Active",
                    "Drug",
                    "Dose",
                    "Start Date",
                    "End Date",
                    "Veterinarian",
                ],
            )
            st.write("Prescription history")
            st.dataframe(
                df,
                height=245,
                use_container_width=True,
                column_config={
                    "Active": st.column_config.CheckboxColumn(
                        help="Prescription is still active",
                        default=False,
                    )
                },
            )

            # Select drug
            result = vet.get_drugs(cursor)
            drugs = dict(result)

            with st.form("prescription_form"):
                # options = list(drugs)
                drug = st.selectbox("Select a drug", drugs, key="drug").lower()

                # Input dose
                dose = st.text_input("Write the dose", key="dose")

                # Input end date
                end_date = st.date_input(
                    "Select prescription's end date", key="presc_end_date"
                )

                submit = st.form_submit_button(
                    "Insert prescription",
                    on_click=lambda: handle_insert_prescription(
                        cursor,
                        drug_id=drugs[st.session_state.drug],
                        animal_id=animals[animal],
                        end_date=st.session_state.presc_end_date,
                        dose=st.session_state.dose,
                    ),
                )


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
        if st.session_state.error != "":
            with st.sidebar.form("error_form"):
                st.warning("MYSQL Error: {}".format(st.session_state.error), icon="⚠️")
                submit = st.form_submit_button(
                    "Clear error message",
                    on_click=lambda: clear_error(),
                )


if __name__ == "__main__":
    main()
