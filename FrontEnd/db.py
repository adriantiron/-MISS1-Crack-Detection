import hashlib as hl
import psycopg2
import decorators


# -1 = already exists; 1 = success
@decorators.db_decorator
def add_user(usern, pw):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="password",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        m = hl.md5(pw.encode('utf-8'))
        cursor.execute("INSERT INTO users(username, passhash, type) VALUES(%s, %s, 'NORMAL');", (usern, m.hexdigest()))
        conn.commit()

        cursor.close()
        conn.close()
        return 1
    except psycopg2.Error as error:
        if error.pgcode == '23505':
            return -1
        else:
            print("Error while connecting to PostgreSQL:", error)


# print(add_user('user1', 'pw1'))
# -1 = wrong password; 0 = no user with that name in db; 1 = all good
@decorators.db_decorator
def login_check(usn, pw):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="password",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        m = hl.md5(pw.encode('utf-8'))
        cursor.execute("SELECT * FROM users where username = %s", (usn,))
        user_record = cursor.fetchone()
        if user_record is None:
            return -1
        elif m.hexdigest() != user_record[1]:
            return 0

        cursor.close()
        conn.close()
        return 1
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)


# print(login_check('user1', 'pw1'))

def delete():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="password",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users;")
        conn.commit()

        cursor.close()
        conn.close()
        return 1
    except psycopg2.Error as error:
        if error.pgcode == '23505':
            return -1
        else:
            print("Error while connecting to PostgreSQL:", error)


# 0 = normal user; 1 = admin user
@decorators.db_decorator
def user_type_check(usn):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="password",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users where username = %s", (usn,))
        user_record = cursor.fetchone()
        if user_record is None:
            return -1
        elif user_record[2] == "NORMAL":
            return 0
        elif user_record[2] == "ADMIN":
            return 1

        cursor.close()
        conn.close()
        return 1
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)