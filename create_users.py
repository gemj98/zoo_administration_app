from authenticator import Authenticator
import mysql.connector
from config import config as DBconfig

db = mysql.connector.connect(**DBconfig)
cursor = db.cursor()
auth = Authenticator(cursor)

auth.create_user(username="vet", password="1", ssn="535-08-5848")
db.commit()
auth.create_user("admin", "1", "761-60-4472")
db.commit()
auth.create_user("security", "1", "377-24-8838")
db.commit()

db.close
