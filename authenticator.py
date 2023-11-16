import bcrypt
import logging
import mysql.connector

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s {%(name)s} [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler = logging.FileHandler("app_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Authenticator:
    def __init__(self, cursor):
        self.status = False
        self.username = ""
        self.result = ""
        self.cursor = cursor
        self.emp_name = ""
        self.emp_ssn = ""

    def print(self):
        print("Status: {}".format(self.status))
        print("Username: {}".format(self.username))

    def login(self, username, password):
        if self.login == True:
            logger.warning("Login into app: Already login")
            return (self.login, self.username, self.role, self.emp_name, self.emp_ssn)
        login_query = """
        SELECT password FROM user
        WHERE username=%s
        """
        login_data = [username]
        self.cursor.execute(login_query, login_data)
        result = self.cursor.fetchall()

        if len(result) == 0:
            logger.info("Login into app: No user found")
            return (False, "", "", "", "")
        else:
            hashed_password = result[0][0].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                role_query = """
                SELECT position, Ename , ssn FROM user NATURAL JOIN employee
                WHERE username=%s
                """
                role_data = [username]
                self.cursor.execute(role_query, role_data)
                result = self.cursor.fetchall()[0]
                role = result[0]
                emp_name = result[1]
                emp_ssn = result[2]

                self.status = True
                self.username = username
                self.role = role
                self.emp_name = emp_name
                self.emp_ssn = emp_ssn
                logger.info("Login into app as role={}: Success".format(self.role))
                return (True, username, role, emp_name, emp_ssn)
            else:
                logger.info("Login into app: User and password do not match")
                return (False, "", "", "", "")

    def logout(self):
        self.status = False
        self.username = ""
        logger.info("Logout")

    def create_user(self, username, password, ssn):
        log_msg = "Creating new user: "
        check_user_query = """
        SELECT username FROM user
        WHERE username=%s
        """
        check_user_data = [username]
        self.cursor.execute(check_user_query, check_user_data)
        result = self.cursor.fetchall()

        if len(result) != 0:
            logger.info("{}User already exists".format(log_msg))
            return (False, "")
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            create_user_query = """
            INSERT INTO user (username, password, ssn)
            VALUES (%s, %s, %s)
            """
            create_user_data = [username, hashed_password, ssn]
            try:
                self.cursor.execute(create_user_query, create_user_data)
            except mysql.connector.Error as err:
                logger.info("{}{}".format(log_msg, err.msg))
            else:
                logger.info("{}Success".format(log_msg))
