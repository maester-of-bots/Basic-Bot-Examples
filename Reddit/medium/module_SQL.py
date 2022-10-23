import sqlite3
from pathlib import Path

# Initial local file config
dbname = "hotfuzz.db"
dbfolder = "db/"

# Create the local database folder if it doesn't exist
Path(dbfolder).mkdir(parents=True, exist_ok=True)


def sqlite_connect():
    """
    Create a local connection to the local database
    """

    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)
    conn.row_factory = lambda cursor, row: row[0]


def init_sqlite():
    """
    Connect to the local database and initialize Hot Fuzz tables.

    Swearbox table tracks specific users and how much they've contributed to the church roof
    comments table tracks all comment IDs that the bot has read / replied to
    """

    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE swearbox (username text, total float )''')
    c.execute('''CREATE TABLE comments (id text)''')


def getUserList():
    """Get all users from the swearbox table

    :return list: username.
    """

    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT username FROM swearbox""")
    result = c.fetchall()
    return result


def getCharges(username):
    """Get total church roof donations for a specific user

    :param str username:  The user to search the database for
    :return int: How much the user owes the swear jar.
    """

    sqlite_connect()
    c = conn.cursor()
    q = [(username)]
    c.execute("""SELECT total FROM swearbox WHERE username=?""", q)
    result = c.fetchall()
    return result[0]


def writeCharges(username, total):
    """Record user donation to the swearbox table

    :param str username:  The username associated with the donation
    :param str total:  The user's total donation amount
    """

    userList = getUserList()
    if username in userList:
        currentCount = getCharges(username)
        newCount = currentCount + total
        command = '''UPDATE swearbox SET total=? WHERE username=?'''
        q = [(newCount), (username)]
    else:
        command = '''INSERT INTO swearbox('username','total') VALUES(?,?)'''
        q = [(username), (total)]
    sqlite_connect()
    c = conn.cursor()
    c.execute(command, q)
    conn.commit()
    conn.close()


def getComments():
    """Get all comment IDs from the comments table

    :return list: All comment IDs.
    """

    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT id FROM comments""")
    result = c.fetchall()
    return result


def writeComment(id):
    """Write a comment ID to the comments table

    :param str id:  The comment ID to record
    """

    sqlite_connect()
    c = conn.cursor()
    q = [(id)]
    c.execute('''INSERT INTO comments('id') VALUES(?)''', q)
    conn.commit()
    conn.close()


# Initialize the database if it's not already done
try:
    init_sqlite()
except:
    pass
