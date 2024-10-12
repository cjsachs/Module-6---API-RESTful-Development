# 1. pip install mysql-connector-python
import mysql.connector

# 2. Create db_connection function
def db_connection():
    # create try, except block for connection
    try:
        # attempt to connect
        db = mysql.connector.connect(
            database='students_db',
            user='root',
            password='cjsachs',
            host='localhost'
        )
        
        if (db.is_connected()):
            print('Successfully connected to MySQL Database!')
            return db
    except:
        print(f'Couldnt connect to the MySQL Database! {mysql.connector.Error}')
        return None
        