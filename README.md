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

- Run DB_App/create_database.py to create the database and populate with initial data.
- To run streamlit app use:

```
  streamlit run DB_App/app.py
```
