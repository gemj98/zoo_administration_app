# zoo_administration_app

## Starting the app

- Clone the repository.
- Create a db_config.py with the following format:

config = {
    "user": "YOUR_MYSQL_USER",
    "password": "YOUR_PASSWORD_FOR_MYSQL",
    "host": "localhost",
    "port": 3306,
    "database": "zoo",
}
  
- Run zoo_db_creation.sql to create the zoo database.
- Run create_users.py to insert users into zoo database.
- To run streamlit use: streamlit run app.py
