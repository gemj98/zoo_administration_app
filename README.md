# Zoo Administration App

## Starting the app

- Clone the repository.
- Create a config.py with the following format in the root folder:

```
config = {
    "user": "YOUR_MYSQL_USER",     // replace with your user for MYSQL, default is root
    "password": "YOUR_PASSWORD_FOR_MYSQL",    //replace with your password
    "host": "localhost",
    "port": 3306,            // 3306 is the default port for MYSQL, replace if selected anotehr one
    "database": "zoo",
}
```

- Run create_database.py to create the database and populate with initial data. users into zoo database.
- To run streamlit app use:

```
  streamlit run app.py
```
