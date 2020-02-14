import sys
from mysql.connector import MySQLConnection, Error
from mysql_client.python_mysql_dbconfig import read_db_config
import datetime


def sql_worker(sql_query, database, ssl=False):
    result = []
    try:
        dbconfig = read_db_config(filename='mysql_client/config.ini', section=database)

        if ssl==True:
            dbconfig['ssl_ca'] = ''

        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        row = cursor.fetchone()

        if row is None:
            print('ERROR. QUERY RETURNS EMPTY RESULTS')
            result = None

        while row is not None:
            #just a whole bunch of stuff to prevent type and encoding errors

            row = [el.decode('utf-8', errors='ignore') if isinstance(el, bytearray) else el for el in row]

            row = [el.isoformat() if isinstance(el, datetime.datetime) else el for el in row]
            #row = [str(el) if isinstance(el, int) else el for el in row]
            result.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return result

def sql_insert(sql_query, database):



    try:
        db_config = read_db_config(filename='mysql_client/config.ini', section=database)
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(sql_query)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
