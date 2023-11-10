from authenticator import Authenticator
import mysql.connector
from config.db_config import config as DBconfig

db = mysql.connector.connect(**DBconfig)
auth = Authenticator(db)

auth.create_user("vet", "1", "535-08-5848")
auth.create_user("admin", "1", "761-60-4472")
auth.create_user("security", "1", "377-24-8838")
auth.print()
auth.login("z", "Z")
auth.print()
auth.login("a", "A")
auth.print()
auth.login("2", "2")
auth.print()
print(auth.login("admin", "1"))
