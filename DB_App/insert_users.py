# SJSU CMPE 138 FALL 2023 TEAM10

import mysql.connector
from authenticator import Authenticator
from config import config as DBconfig

db = mysql.connector.connect(**DBconfig)
cursor = db.cursor()
auth = Authenticator(cursor)

# Create users
auth.create_user(username="dwilson", password="1", ssn="535-08-5848")  # vet
auth.create_user("scollins", "1", "761-60-4472")  # admin
auth.create_user("ggarcia", "1", "377-24-8838")  # security
auth.create_user("jsmith", "1", "867-43-6911")  # trainer
auth.create_user("omiller", "1", "514-24-9839")  # feeder
auth.create_user("pwilliams", "1", "628-43-7850")  # habitat_manager
auth.create_user("fevans", "1", "593-63-0610")  # tour_guide
db.commit()

db.close()
