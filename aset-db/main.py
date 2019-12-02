import hashlib as hl
import psycopg2


def add_user(usern, pw):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        m = hl.md5(pw.encode('utf-8'))
        cursor.execute("INSERT INTO users(username, passhash) VALUES(%s, %s);", (usern, m.hexdigest()))
        conn.commit()
        print("Succeeded in inserting record in the table!")

        cursor.close()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


# -1 = wrong password; 0 = no user with that name in db; 1 = all good
def login_check(usn, pw):
    try:
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="127.0.0.1",
                                port="5432",
                                database="crack-detection")
        cursor = conn.cursor()
        m = hl.md5(pw.encode('utf-8'))
        cursor.execute("SELECT * FROM users where username = %s", (usn,))
        user_record = cursor.fetchone()
        print(user_record[1], m.hexdigest())
        if user_record is None:
            return -1
        elif m.hexdigest() != user_record[1]:
            return 0

        cursor.close()
        conn.close()
        return 1
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


print(login_check('user1', 'pw1'))
