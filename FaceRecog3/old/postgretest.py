
import psycopg2
from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="personauser",
                                  # пароль, который указали при установке PostgreSQL
                                  password="pgpwd4persona",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="personadb")

    cursor = connection.cursor()
    # # Выполнение SQL-запроса для вставки данных в таблицу
    # insert_query = """ INSERT INTO z1frame (id, data, milliseconds ,timestr) VALUES (1, 'Iphone12', 1100,'ggg')"""
    # cursor.execute(insert_query)



    connection.commit()
    print("1 запись успешно вставлена")
except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into mobile table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")