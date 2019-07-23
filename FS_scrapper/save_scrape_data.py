import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
import json

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'fsport',
    'raise_on_warnings': True
}
def insert_slates_into_db(slate_data):

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        for slate in slate_data:
            sport_type = slate['sportType']
            slate_name = '' if slate['title'] == '' else slate['title'] + " " + str(slate['gameCount']) + " games"
            slate_time = slate['time']
            salary = json.dumps(slate['data'])

            data_salary = ('DraftKings', sport_type, slate_name, slate_time, salary)

            sql_select_query = """select absid, slate_name from slates where site = %s and slate_time LIKE %s and sport_type = %s"""
            
            cursor.execute(sql_select_query, ('DraftKings', slate_time, sport_type))
            
            records = cursor.fetchall()

            count = cursor.rowcount

            cursor.close()

            cursor = connection.cursor()
            
            add_salary_query = ""

            if count < 1:
                add_salary_query = """INSERT INTO slates (site, sport_type, slate_name, slate_time, salary) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(add_salary_query, data_salary)
                connection.commit()
            else:
                for row in records:
                    if row[1] == slate_name:
                        add_salary_query = """Update slates set salary = %s where absid = %s"""
                        data_salary = (salary, row[0])
                        cursor.execute(add_salary_query, data_salary)
                        connection.commit()
            
    except mysql.connector.Error as error:
        connection.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):    
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_projection_into_db(slate_data, sport_type, site):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cur_date = "%" + datetime.today().strftime('%Y-%m-%d') + "%"
        if sport_type == "PGA":
            # slate_name = '' if slate['title'] == '' else slate['title'] + " " + str(slate['gameCount']) + " games"
            # slate_time = slate['time']
            update_projection_query = """Update slates set projection = %s where sport_type = %s and site = %s and slate_time LIKE %s"""

            data_projection = (json.dumps(slate_data), sport_type, site, cur_date)
            cursor.execute(update_projection_query, data_projection)
            connection.commit()
        else:
            for key, value in slate_data.items():
                update_projection_query = """Update slates set projection = %s where sport_type = %s and site = %s and slate_time LIKE %s"""
                data_projection = (json.dumps(value), sport_type, site, cur_date)
                cursor.execute(update_projection_query, data_projection)
                connection.commit()
        
    except mysql.connector.Error as error:
        connection.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):    
            cursor.close()
            connection.close()
            print("MySQL connection is closed")