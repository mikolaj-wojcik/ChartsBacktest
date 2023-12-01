import sqlite3
from sqlite3 import Error


def connect(database):
    try:
        conn = sqlite3.connect(database)

    except:
        pass

    finally:
        pass