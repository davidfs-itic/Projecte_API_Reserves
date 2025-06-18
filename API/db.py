#import mysql.connector
#from mysql.connector import pooling
import pymysql

# Configura la connexió a MariaDB
db_config = {
    'host': 'mariadb',
    'user': 'david',
    'password': '1357924680',
    'database': 'reserves',
    'collation': 'utf8mb4_general_ci'
}

# Pool de connexions
#db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

def get_db_connection():
#    return db_pool.get_connection()
    return pymysql.connect(
        host='mariadb',
        user='david',
        password='1357924680',
        database='reserves',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # perquè els resultats siguin dicts
    )