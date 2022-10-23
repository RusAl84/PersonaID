import time
import psycopg2
import datetime

if __name__ == "__main__":
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    connection.autocommit = True

    minutes = 10

    while True:
        milliseconds = int(time.time() * 1000) - 1000 * 60 * minutes
        print(milliseconds)
        dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
        print(dt)
        cursor = connection.cursor()
        sql_delete_query = f"DELETE FROM public.z1frame WHERE milliseconds < {milliseconds};"
        cursor.execute(sql_delete_query)
        connection.commit()
        time.sleep(0.5)
        sql_delete_query = f"Delete from public.zdata WHERE milliseconds < {milliseconds};"
        cursor.execute(sql_delete_query)
        connection.commit()
        time.sleep(0.5)
        sql_delete_query = f"Delete from public.zdash WHERE milliseconds < {milliseconds};"
        cursor.execute(sql_delete_query)
        connection.commit()
        time.sleep(5)
    connection.commit()
    connection.close()
