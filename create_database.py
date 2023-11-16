from authenticator import Authenticator
import mysql.connector
from config import config as DBconfig
import subprocess


def runMysqlScript(script_path):
    host = "-h" + DBconfig["host"]
    user = "-u" + DBconfig["user"]
    password = "-p" + DBconfig["password"]
    with open(script_path) as input_file:
        result = subprocess.run(
            ["mysql", host, user, password],
            stdin=input_file,
            capture_output=True,
        )


# Create database
runMysqlScript("zoo_creation_all.sql")

db = mysql.connector.connect(**DBconfig)
cursor = db.cursor()
auth = Authenticator(cursor)

# Create users
auth.create_user(username="veterinarian", password="1", ssn="535-08-5848")
auth.create_user("admin", "1", "761-60-4472")
auth.create_user("security", "1", "377-24-8838")
auth.create_user("trainer", "1", "867-43-6911")
auth.create_user("feeder", "1", "514-24-9839")
auth.create_user("habitat_manager", "1", "628-43-7850")
auth.create_user("tour_guide", "1", "593-63-0610")
db.commit()

db.close()
