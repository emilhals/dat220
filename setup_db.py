import sqlite3
from sqlite3 import Error

database = r"./database.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

##### CREATE TABLES ######## 
create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(20) NOT NULL,
                                gender CHAR(1) NOT NULL check(gender in ('F','M','O')),
                                email VARCHAR(30) NOT NULL,
                                password VARCHAR(20) NOT NULL
                                created DATE DEFAULT current_timestamp
                            );"""
                            
create_communities_table = """CREATE TABLE IF NOT EXISTS communities (
                                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                about TINYTEXT,
                                users 
                                FOREIGN KEY ()
                            );"""

create_communityuser_table = """ CREATE TABLE IF NOT EXISTS CommunityUser (
                                community int NOT NULL,
                                user int NOT NULL,
                                FOREIGN KEY (community) REFERENCES community(id) ON DELETE set null
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE set null

                            );"""

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, create_users_table)
        create_table(conn, sql_create_businesses_table)
        create_table(conn, sql_create_bookings_table)

        conn.close()


if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()