import sqlite3
from pathlib import Path

# Initial local file config
dbname = "botnameorsomething.db"
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
    Connect to the local database and initialize the database.

    comments table tracks all comment IDs that the bot has read / replied to
    """

    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE comments (id text, bot text)''')


def checkDB(id,bot):
    sqlite_connect()
    c = conn.cursor()
    q = [(id),(bot)]
    c.execute("""SELECT * FROM comments WHERE id = ? AND bot = ?""", q)
    result = c.fetchone()
    if result:
        print("Found one")
        return True
    else:
        return False

def writeComment(id,bot):
    """Write a comment ID to the comments table

    :param str id:  The comment ID to record
    """

    sqlite_connect()
    c = conn.cursor()
    q = [(id), (bot)]
    c.execute('''INSERT INTO comments('id', 'bot') VALUES(?,?)''', q)
    conn.commit()
    conn.close()



# Initialize the database if it's not already done
try:
    init_sqlite()
except:
    pass
