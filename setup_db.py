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
# VARCHAR(20) = TEXT for SQLite, so i swapped them for simplicity
# On delete set null -> if creator deletes account, community remains and creator = null
# On delete cascade -> if user deletes community, all posts and comments are removed

##### CREATE TABLES ######## 
create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY NOT NULL,
                                username TEXT UNIQUE NOT NULL,
                                gender CHAR(1) NOT NULL check(gender in ('F','M','O')),
                                email VARCHAR UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                created DATE DEFAULT current_timestamp,
                                admin INT NOT NULL DEFAULT 0
                            );"""
                                
create_communities_table = """CREATE TABLE IF NOT EXISTS communities (
                                id INTEGER PRIMARY KEY NOT NULL,
                                about TINYTEXT,
                                members INT,
                                creator INTEGER NOT NULL,
                                FOREIGN KEY (creator) REFERENCES users(id) ON DELETE SET NULL
                            );"""

create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                id INTEGER PRIMARY KEY NOT NULL,
                                user INTEGER NOT NULL,
                                img LONGBLOB, 
                                text TINYTEXT,
                                likes INT,
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                            );"""

create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                id INTEGER PRIMARY KEY NOT NULL,
                                post INTEGER NOT NULL,
                                user INTEGER NOT NULL,
                                reply INTEGER NOT NULL,
                                img LONGBLOB, 
                                text TINYTEXT,
                                likes INT,
                                FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                                FOREIGN KEY (reply) REFERENCES comments(id) ON DELETE CASCADE
                            );"""

create_likeComment_table = """CREATE TABLE IF NOT EXISTS likeComment (
                                user INTEGER NOT NULL,
                                comment INTEGER NOT NULL,
                                PRIMARY KEY (user, comment),
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                                FOREIGN KEY (comment) REFERENCES comments(id) ON DELETE CASCADE
                            );"""

create_likePost_table = """CREATE TABLE IF NOT EXISTS likePost (
                                user INTEGER NOT NULL,
                                post INTEGER NOT NULL,
                                PRIMARY KEY (user, post),
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                                FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
                            );"""

create_communityuser_table = """ CREATE TABLE IF NOT EXISTS CommunityUser (
                                community INTEGER NOT NULL,
                                user INTEGER NOT NULL,
                                PRIMARY KEY (community, user),
                                FOREIGN KEY (community) REFERENCES communities(id) ON DELETE CASCADE
                                FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
                            );"""

create_communitypost_table = """ CREATE TABLE IF NOT EXISTS CommunityPost (
                                community INTEGER NOT NULL,
                                post INTEGER NOT NULL,
                                PRIMARY KEY (community, post),
                                FOREIGN KEY (community) REFERENCES communities(id) ON DELETE CASCADE
                                FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
                            );"""
create_follow_table = """ CREATE TABLE IF NOT EXISTS follow (
                                follower INTEGER NOT NULL,
                                follows INTEGER NOT NULL,
                                FOREIGN KEY (follower) REFERENCES users(id) ON DELETE CASCADE
                                FOREIGN KEY (follows) REFERENCES users(id) ON DELETE CASCADE
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
        create_table(conn, create_users_table)
        create_table(conn, create_communities_table)
        create_table(conn, create_posts_table)
        create_table(conn, create_comments_table)
        create_table(conn, create_likeComment_table)
        create_table(conn, create_likePost_table)
        create_table(conn, create_communityuser_table)
        create_table(conn, create_communitypost_table)
        create_table(conn, create_follow_table)
        conn.close()

if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()


#Add user to community:
# INSERT INTO community_users (community.id, users.id) VALUES (1, 2);
#Add post to community:
# INSERT INTO community_posts (community.id, posts.id) VALUES (1, 2);
#Add comment to post:
# INSERT INTO comments (posts.id, users.id, reply.id, img, text) VALUES (1, 2, 3, 'img', 'text');

#Find amount of likes members:
# COUNT(users.id) FROM likeComment
# COUNT(users.id) FROM likePost
# COUNT(communityUsers) where community = ...

#Admin check:
#  SELECT * FROM users WHERE admin = TRUE; -> Fetches rows where admin = 1

#Get all users in a community:
# SELECT users.* FROM users
# JOIN CommunityUsers ON users.id = CommunityUsers.user
#       WHERE CommunityUsers.community = ..; <- use to get one specific

#Get all posts in a community:
# SELECT posts.* FROM posts
# JOIN CommunityPosts ON posts.id = CommunityPosts.post
#       WHERE CommunityPosts.community = ...; <- use to get one specific

#Get all comments on a post:
# SELECT comments.* FROM comments
# JOIN posts ON comments.post = posts.id
#       WHERE posts.id = ...; <- use to get one specific