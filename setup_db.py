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


# INTEGER PRIMARY KEY = autoincrementing id
# SQLite doesn't AUTO_INCREMENT, but INTEGER PRIMARY KEY does the same and increments!
# INT and INTEGER is not same, int is stored as NUMERIC and integer as 8-bit integer
#  only INTEGER allows auto-incrementing = PK. Therefore
#  all ref:FK=INT is also INTEGER, even though INT works it's not ideal
# UNIQUE usernames, emails and ids
# ADMIN = 1 if admin, 0 if not. SQLite doesn't support boolean, 1 and 0 works the same though.
#   -> BOOLEAN NOT NULL DEFAULT 0 works as 1 or 0!
# VARCHAR(20) = TEXT for SQLite, so i swapped them for simplicity
# On delete set null -> if creator deletes account, community remains and creator = null
# On delete cascade -> if user deletes community, all posts and comments are removed
# TINYTEXT = VARCHAR(255), not supported by SQLite. No error pga sql type affinity = not enforced
#   -> Swapped for TEXT=Varchar(255)

##### CREATE TABLES ######## 
create_user_table = """CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY NOT NULL,
                                username TEXT UNIQUE NOT NULL,
                                gender CHAR(1) NOT NULL check(gender in ('F','M','O')),
                                email VARCHAR UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                created DATE DEFAULT current_timestamp,
                                admin BOOLEAN NOT NULL DEFAULT 0
                            );"""
                                
create_community_table = """CREATE TABLE IF NOT EXISTS community (
                                id INTEGER PRIMARY KEY NOT NULL,
                                about TEXT,
                                creator INTEGER NOT NULL,
                                FOREIGN KEY (creator) REFERENCES user(id) ON DELETE SET NULL
                            );"""

create_post_table = """CREATE TABLE IF NOT EXISTS post (
                                id INTEGER PRIMARY KEY NOT NULL,
                                user INTEGER NOT NULL,
                                img LONGBLOB, 
                                text TEXT,
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
                            );"""

create_comment_table = """CREATE TABLE IF NOT EXISTS comment (
                                id INTEGER PRIMARY KEY NOT NULL,
                                post INTEGER NOT NULL,
                                user INTEGER NOT NULL,
                                reply INTEGER DEFAULT NULL,
                                img LONGBLOB, 
                                text TEXT,
                                FOREIGN KEY (post) REFERENCES post(id) ON DELETE CASCADE
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
                                FOREIGN KEY (reply) REFERENCES comment(id) ON DELETE CASCADE
                            );"""

create_commentLike_table = """CREATE TABLE IF NOT EXISTS commentLike (
                                user INTEGER NOT NULL,
                                comment INTEGER NOT NULL,
                                PRIMARY KEY (user, comment),
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
                                FOREIGN KEY (comment) REFERENCES comment(id) ON DELETE CASCADE
                            );"""

create_postLike_table = """CREATE TABLE IF NOT EXISTS postLike (
                                user INTEGER NOT NULL,
                                post INTEGER NOT NULL,
                                PRIMARY KEY (user, post),
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
                                FOREIGN KEY (post) REFERENCES post(id) ON DELETE CASCADE
                            );"""

create_communityUser_table = """ CREATE TABLE IF NOT EXISTS CommunityUser (
                                community INTEGER NOT NULL,
                                user INTEGER NOT NULL,
                                PRIMARY KEY (community, user),
                                FOREIGN KEY (community) REFERENCES community(id) ON DELETE CASCADE
                                FOREIGN KEY (user) REFERENCES user(id) ON DELETE CASCADE
                            );"""

create_communityPost_table = """ CREATE TABLE IF NOT EXISTS CommunityPost (
                                community INTEGER NOT NULL,
                                post INTEGER NOT NULL,
                                PRIMARY KEY (community, post),
                                FOREIGN KEY (community) REFERENCES community(id) ON DELETE CASCADE
                                FOREIGN KEY (post) REFERENCES post(id) ON DELETE CASCADE
                            );"""
create_follow_table = """ CREATE TABLE IF NOT EXISTS follow (
                                follower INTEGER NOT NULL,
                                follows INTEGER NOT NULL,
                                PRIMARY KEY (follower, follows),
                                FOREIGN KEY (follower) REFERENCES user(id) ON DELETE CASCADE
                                FOREIGN KEY (follows) REFERENCES user(id) ON DELETE CASCADE
                            );"""
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(f"Error creating table: {e}")

def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, create_user_table)
        create_table(conn, create_community_table)
        create_table(conn, create_post_table)
        create_table(conn, create_comment_table)
        create_table(conn, create_commentLike_table)
        create_table(conn, create_postLike_table)
        create_table(conn, create_communityUser_table)
        create_table(conn, create_communityPost_table)
        create_table(conn, create_follow_table)
        conn.close()

############# Relationships #############
# follows, likes and community joins.
def create_follow(connection, follow):
    sql = ''' INSERT INTO follow(follower, follows) VALUES(?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (follow.follower, follow.follows))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

def create_commentLike(connection, commentLike):
    sql = ''' INSERT INTO commentLike(user, comment) VALUES(?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (commentLike.user, commentLike.comment))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

def create_postLike(connection, postLike):
    sql = ''' INSERT INTO postLike(user, post) VALUES(?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (postLike.user, postLike.post))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

def create_communityPost(connection, communityPost):
    sql = ''' INSERT INTO CommunityPost(community, post) VALUES(?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (communityPost.community, communityPost.post))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

def create_communityUser(connection, communityUser):
    sql = ''' INSERT INTO CommunityUser(community, user) VALUES(?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (communityUser.community, communityUser.user))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

############# COMMUNITY #############
# community is initially created with communityUser
def create_community(connection, community):
    sql = ''' INSERT INTO community(about, creator) VALUES(?,?) ''' 
    try:
        cur = connection.cursor()
        cur.execute(sql, (community.about, community.creator))
        community.id = cur.lastrowid # INTEGER PRIMARY KEY // gets ID from last row
        create_communityUser(community.id, community.creator) # add creator to communityUser table
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

# post is initially created with communityPost
# when crating a post you need to pass info on what community it comes from to this function
def create_post(connection, post, communityPost):
    sql = ''' INSERT INTO post(user, img, text) VALUES(?,?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (post.user, post.img, post.text))
        post.id = cur.lastrowid # INTEGER PRIMARY KEY // gets ID from last row
        create_communityPost(communityPost.community, post.id)
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

# comment creation
# when crating a comment you need to pass info on what post 
# it comes from to this function and/if it is a reply or not.
# Rreply is stored as an ID for a comment, or as 0
def create_comment(connection, comment):
    sql = ''' INSERT INTO comment(user, post, reply, text)
                              VALUES(?,?,?,?) '''
    try:
        cur = connection.cursor()
        # Check if the post exists
        cur.execute(sql, (comment.user, comment.post, comment.reply, comment.text))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()

############# USER #############
# user registration
def create_user(connection, user):
    sql = ''' INSERT INTO users(username, gender, email, password, admin)
        VALUES(?,?,?,?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, (user.username, user.gender, user.email, user.password, user.admin))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(e)
    finally:
        cur.close()
        
# user login
def login(connection, username, password):
    sql = ''' SELECT username, password FROM users 
    WHERE username=? AND password=? ''' 
    try:
        cur = connection.cursor()
        cur.execute(sql, (username, password,))
        connection.commit()
    
        row = cur.fetchone()
        if row:
            username, password = row
            
            return {
                "username": username,
                "password": password
            }        
    except Error as e:
        print(e)
    finally:
        cur.close()

if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()