import mysql.connector
import bcrypt


class Authenticator:
    def __init__(self, cursor):
        self.status = False
        self.username = ""
        self.result = ""
        self.cursor = cursor

    def print(self):
        print("Status: {}".format(self.status))
        print("Username: {}".format(self.username))

    def login(self, username, password):
        login_query = """
        SELECT password FROM user
        WHERE username=%s
        """
        login_data = [username]
        self.cursor.execute(login_query, login_data)
        result = self.cursor.fetchall()

        if len(result) == 0:
            print("*No user found.")
            return (False, "", "", "", "")
        else:
            hashed_password = result[0][0].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                print("Login succesful. Welcome {}.".format(username))

                role_query = """
                SELECT position, name , ssn FROM user NATURAL JOIN employee
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
                self.emp_name = emp_ssn
                return (True, username, role, emp_name, emp_ssn)
            else:
                print("*User and password do not match.")
                return (False, "", "", "", "")

    def logout(self):
        self.status = False
        self.username = ""

    def create_user(self, username, password, ssn):
        check_user_query = """
        SELECT username FROM user
        WHERE username=%s
        """
        check_user_data = [username]
        self.cursor.execute(check_user_query, check_user_data)
        result = self.cursor.fetchall()

        if len(result) != 0:
            print("*User already exists.")
            return (False, "")
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            create_user_query = """
            INSERT INTO user (username, password, ssn)
            VALUES (%s, %s, %s)
            """
            create_user_data = [username, hashed_password, ssn]
            self.cursor.execute(create_user_query, create_user_data)
