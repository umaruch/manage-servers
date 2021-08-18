from os import path
from os import path
import sqlite3

from . import utils
import settings

if path.exists(settings.SQLITE_FILE):
    db_connection = sqlite3.connect(settings.SQLITE_FILE, check_same_thread=False)
    db_connection.execute("PRAGMA foreign_keys")
else:
    db_connection = sqlite3.connect(settings.SQLITE_FILE, check_same_thread=False)
    db_connection.execute("PRAGMA foreign_keys")
    utils.create_all(db_connection)
