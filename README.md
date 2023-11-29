# SJSU CMPE 138 FALL 2023 TEAM10

# Zoo Administration App

## Starting the app

- Clone the repository.
- Create a config.py with the following format inside DB_App folder:

```
config = {
    "user": "YOUR_MYSQL_USER",     // replace with your user for MYSQL, default is root
    "password": "YOUR_PASSWORD_FOR_MYSQL",    //replace with your password
    "host": "localhost",
    "port": 3306,            // 3306 is the default port for MYSQL, replace if selected another one
    "database": "zoo",
}
```

- To create the database and populate with initial data use:

```
python DB_App/create_database.py
```

- ONLY IF ERROR while running DB_App/create_database.py. Procede to run the following SQL scrypts manually:
  - tables_creation.sql
  - animal_check_trigger.sql
  - load_initial_data.sql
  - Run ```python DB_App/create_users.py```

- To run streamlit app use:

```
  streamlit run DB_App/app.py
```
