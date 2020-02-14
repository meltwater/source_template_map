from mysql.connector import MySQLConnection, Error
from mysql_client.python_mysql_dbconfig import read_db_config
import datetime


def sql_worker(sql_query):
    result = []
    try:
        dbconfig = read_db_config(filename='mysql_client/config.ini', section='magenta')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        row = cursor.fetchone()

        if row is None:
            print('ERROR. QUERY RETURNS EMPTY RESULTS')

        while row is not None:
            row = [el.decode('utf-8') if isinstance(el, bytearray) else el for el in row]
            row = [el.isoformat() if isinstance(el, datetime.datetime) else el for el in row]
            row = [str(el) if isinstance(el, int) else el for el in row]
            result.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return result
