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

def get_db_slate(slate):
    global connection    
    try:
        # slate = { "site": "DraftKings", "sport_type": "MLB"}
        slate_data = json.loads(slate)
        slate_list = list()

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        sql_select_query = """select absid, slate_name, slate_time from slates where site = %s and slate_time LIKE %s and sport_type = %s"""
        
        cur_date = "%" + datetime.today().strftime('%Y-%m-%d') + "%"
        cursor.execute(sql_select_query, (slate_data["site"], cur_date, slate_data["sport_type"], ))
        records = cursor.fetchall()
        
        for row in records:
            slate_info = {}
            slate_info["id"] = row[0]
            slate_info["slate_name"] = row[2][11:16] + " " + row[1]
            slate_list.append(slate_info)

        
    except mysql.connector.Error as error:
        connection.rollback()
        print("Failed to load Slate data {}".format(error))
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
