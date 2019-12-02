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
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed...")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


add_user('user1', 'pw1')
