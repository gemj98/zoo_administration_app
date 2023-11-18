# SJSU CMPE 138 FALL 2023 TEAM10

import streamlit as st
import mysql.connector
import pandas as pd
from authenticator import Authenticator
from config import config as DBconfig
import queries.vet_queries as vet
import queries.admin_queries as admin
import queries.animal_habitat_queries as animalHab
import queries.security as security
import queries.tour_guide as tour_guide

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
    st.session_state.error = ""
    st.session_state.sql_result = ""


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

def handle_insert_meal_record(cursor, specie_id):
    st.session_state.error = animalHab.insert_meal_record(
        cursor, specie_id
    )
    db.commit()

def handle_update_training_status(cursor, animal_id, training_status):
    st.session_state.error = animalHab.update_animal_status(
        cursor, animal_id, training_status
    )
    db.commit()

def handle_update_temperature(cursor, habitat_id, temperature):
    st.session_state.error = animalHab.update_habitat_temp(
        cursor, habitat_id, temperature
    )
    db.commit()

def handle_sql_query(db, sql_query):
    (st.session_state.sql_result, st.session_state.error) = admin.run_query(
        db, sql_query
    )
    db.commit()

def handle_add_new_tour(cursor, tour_name, max_cap, habitat_id):
    st.session_state.error = tour_guide.add_new_tour(cursor, tour_name, max_cap, habitat_id)
    db.commit()

def handle_modify_tour(cursor, tour_id, habitat_id):
    st.session_state.error = tour_guide.modify_tour_sees(
        cursor, tour_id, habitat_id
        )
    db.commit()

def handle_modify_tour_sees(cursor, tour_id, tour_name, max_cap):
    st.session_state.error = tour_guide.modify_tour(
        cursor, tour_id, tour_name, max_cap
        )
    db.commit()

def handle_provide_tour(cursor, tour_id):
    st.session_state.sql_result, st.session_state.error = tour_guide.provide_tour(
        cursor, tour_id
        )
    db.commit()

def handle_check_visitor_ticket(cursor, ticket):
    st.session_state.sql_result = security.check_visitor_ticket(
        cursor, ticket
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
    menu = ["Home", "SQL Query"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "SQL Query":
            st.subheader("Run a custom query 👨🏻‍💻")
            with st.form("sql_form"):
                # Input sql query
                dose = st.text_input("Write an SQL Query", key="sql_query")

                submit = st.form_submit_button(
                    "Run query",
                    on_click=lambda: handle_sql_query(db, st.session_state.sql_query),
                )

            st.write(st.session_state.sql_result)


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
    menu = ["Home",
            "Check Visitor Ticket",]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Check Visitor Ticket":
            st.subheader("Check Visitor Ticket :admission_tickets:")

            # Select ticket
            result = security.get_ticket_id(cursor)
            tickets = dict(result)
            options = [word.capitalize() for word in list(tickets)]
            selected_ticket = st.selectbox("Select a ticket", options).lower()

            with st.form("check_visitor_ticket"):
                submit = st.form_submit_button(
                    "Check Visitor Ticket",
                    on_click=lambda: handle_check_visitor_ticket(
                        cursor,
                        ticket_id=selected_ticket,
                    ),
                )
            
            st.write(st.session_state.sql_result)

def render_feeder_options():
    menu = ["Home", "Insert meal record"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Insert meal record":
            st.subheader("Insert meal record :turtle:")

            # Select specie
            result = animalHab.get_species(cursor)
            species = dict(result)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options).lower()

            # List past 5 meal records
            result = animalHab.get_meal_records(cursor, species[specie])
            df = pd.DataFrame(result, columns=["Record Date"])
            st.write("Meal Record history")
            st.dataframe(
                df,
                height=245,
                use_container_width=True,
            )
            
            with st.form("meal_record_form"):
                submit = st.form_submit_button(
                    "Insert meal record",
                    on_click=lambda: handle_insert_meal_record(
                        cursor,
                        specie_id=species[specie],
                    ),
                )


def render_trainer_options():
    menu = ["Home", "Update animal training status"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Update animal training status":
            st.subheader("Update animal training status :turtle:")
            
            # Select specie
            result = vet.get_species_single(cursor)
            species = dict(result)
            options = [word.capitalize() for word in list(species)]
            specie = st.selectbox("Select a specie", options).lower()

            # Select animal
            result = animalHab.get_animals_from_specie(cursor, species[specie])
            print(result)
            animals = dict(result)
            options = list(animals)
            animal = st.selectbox("Select an animal", animals)

            # Display current training status
            result = animalHab.get_animal_status(cursor, animals[animal])
            df = pd.DataFrame(result, columns=["Training Status"])
            st.write("Training Status")
            st.dataframe(
                df,
                height=245,
                use_container_width=True,
            )

            result = animalHab.get_status_options(cursor)
            status_options = dict(result)
            options = [word for word in list(status_options)]
            status = st.selectbox("Select a training status", options)
            
            with st.form("training_form"):

                submit = st.form_submit_button(
                    "Update training status",
                    on_click=lambda: handle_update_training_status(
                        cursor,
                        animal_id=animals[animal],
                        training_status=status_options[status]
                    ),
                )



def render_habitat_manager_options():
    menu = ["Home", "Update habitat temperature"]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Update habitat temperature":

            # Select habitat
            result = animalHab.get_habitat(cursor)
            habitats = dict(result)
            options = [word.capitalize() for word in list(habitats)]
            habitat = st.selectbox("Select a habitat", options).lower()

            # Display current temperature
            result = animalHab.get_habitat_temp(cursor, habitats[habitat])
            df = pd.DataFrame(result, columns=["Temperature"])
            st.write("Temperature")
            st.dataframe(
                df,
                height=245,
                use_container_width=True,
            )

            # Input temperature
            temp = st.text_input("Write the temperature", key="temperature")

            with st.form("habitat_form"):
                

                submit = st.form_submit_button(
                    "Update temperature",
                    on_click=lambda: handle_update_temperature(
                        cursor,
                        habitat_id = habitats[habitat],
                        temperature = temp
                    ),
                )            

def render_tour_guide_options():
    menu = ["Home",
            "Add New Tour",
            "Modify Tour",
            "Modify Habitat associated with Tour",
            "Record completed tour",]
    options = st.sidebar.radio("Select an option :dart:", menu)
    match options:
        case "Home":
            greetings()
        case "Add New Tour":
            st.subheader("Add a new tour :walking:")

            # Select habitat id
            result = tour_guide.get_habitat_id(cursor)
            all_habitat = dict(result)

            # Create a form to collect input
            with st.form("add_tour_form"):
                # Input habitat id
                habitat_id = st.selectbox("Select a habitat", all_habitat, key="habitat_id").lower()
                # Input tour name
                tour_name = st.text_input("Tour name: ", key="tour_name")
                # Input tour capacity
                tour_cap = st.text_input("Tour's maximum capacity: ", key="tour_cap")
 
                submit = st.form_submit_button(
                    "Add tour",
                    on_click=lambda: handle_add_new_tour(
                        cursor,
                        tour_name,
                        tour_cap,
                        habitat_id,
                    ),
                )
        
        case "Modify Tour":
            st.subheader("Modify Tour :walking:")
            st.write("You can only modify tours that you're managing.")
            # Select tour_id
            result = tour_guide.get_tour_id(cursor)
            all_tours = dict(result)

            # Create a form to collect input
            with st.form("modify_tour_form"):
                # Input tour id
                tour_id = st.selectbox("Select a tour id", all_tours, key="tour_id").lower()
                # Input tour name
                tour_name = st.text_input("New Tour name: ", key="tour_name")
                # Input tour capacity
                tour_cap = st.text_input("Tour's new maximum capacity: ", key="tour_cap")
 
                submit = st.form_submit_button(
                    "Modify tour",
                    on_click=lambda: handle_modify_tour(
                        cursor,
                        tour_id,
                        tour_name,
                        tour_cap,
                    ),
                )
            
            st.write(st.session_state.error)

        case "Modify Habitat associated with Tour":
            st.subheader("Modify Habitat associated with Tour :guide_dog:")
            st.write("You can only modify tours that you're managing.")
            # Select tour_id
            result = tour_guide.get_tour_id(cursor)
            all_tours = dict(result)

            # Select habitat id
            result = tour_guide.get_habitat_id(cursor)
            all_habitat = dict(result)

            # Create a form to collect input
            with st.form("modify_tour_habitat_form"):
                # Input tour id
                tour_id = st.selectbox("Select a tour id", all_tours, key="tour_id").lower()
                # Input habitat id
                habitat_id = st.selectbox("Select a habitat", all_habitat, key="habitat_id").lower()
 
                submit = st.form_submit_button(
                    "Modify tour habitat",
                    on_click=lambda: handle_modify_tour_sees(
                        cursor,
                        tour_id,
                        habitat_id,
                    ),
                )
            
            st.write(st.session_state.error)

        case "Record completed tour":
            st.subheader("Record a tour that's completed :white_check_mark:")
            st.write("You can only complete tours that you're guiding.")
            # Select tour_id
            result = tour_guide.get_tour_id(cursor)
            all_tours = dict(result)

            # Select habitat id
            result = tour_guide.get_habitat_id(cursor)
            all_habitat = dict(result)

            # Create a form to collect input
            with st.form("modify_tour_habitat_form"):
                # Input tour id
                tour_id = st.selectbox("Select a tour id", all_tours, key="tour_id").lower()
                # Input habitat id
                habitat_id = st.selectbox("Select a habitat", all_habitat, key="habitat_id").lower()
 
                submit = st.form_submit_button(
                    "Complete tour",
                    on_click=lambda: handle_provide_tour(
                        cursor,
                        tour_id,
                    ),
                )
            
            st.write(st.session_state.sql_result)

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
