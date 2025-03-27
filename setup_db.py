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

# on delete cascade => fjern childs til parent. 
##### CREATE TABLES ######## 

# unique usernames, emails and ids
create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(20) UNIQUE NOT NULL,
                                gender CHAR(1) NOT NULL check(gender in ('F','M','O')),
                                email VARCHAR(30) UNIQUE NOT NULL,
                                password VARCHAR(20) NOT NULL,
                                created DATE DEFAULT current_timestamp,
                                admin BOOLEAN,
                            );"""
                                
# On delete not null, not cascade. Dont want to delete communities when deleting a user.   
create_communities_table = """CREATE TABLE IF NOT EXISTS communities (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                about TINYTEXT,
                                users,
                                posts,
                                creator INT NOT NULL,
                                FOREIGN KEY (creator) REFERENCES users(id) ON DELETE NOT NULL
                            );"""

create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                user INT NOT NULL,
                                img LONGBLOB, 
                                text TINYTEXT,
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                            );"""

create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                post INT NOT NULL,
                                user INT NOT NULL,
                                reply INT NOT NULL,
                                img LONGBLOB, 
                                text TINYTEXT,
                                FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                                FOREIGN KEY (reply) REFERENCES comments(id) ON DELETE CASCADE
                            );"""

create_communityuser_table = """ CREATE TABLE IF NOT EXISTS CommunityUser (
                                community INT NOT NULL,
                                user INT NOT NULL,
                                PRIMARY KEY (community, user),
                                FOREIGN KEY (community) REFERENCES communities(id) ON DELETE  CASCADE
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                            );"""

create_communitypost_table = """ CREATE TABLE IF NOT EXISTS CommunityPost (
                                community INT NOT NULL,
                                post INT NOT NULL,
                                PRIMARY KEY (community, post),
                                FOREIGN KEY (community) REFERENCES communities(id) ON DELETE CASCADE
                                FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
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