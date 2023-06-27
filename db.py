import sqlite3
import logging

database = sqlite3.connect("china_travel.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table that displays which client belongs which manager
    cursor.execute('''CREATE TABLE associated_managers (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR (30),
        manager_name VARCHAR (30),
        manager_username VARCHAR (30)
    )''')
except:
    logging.error('Associated_managers table already exists.')

try:
    # creates table with information about managers
    cursor.execute('''CREATE TABLE managers (
        id INTEGER PRIMARY KEY,
        manager_id VARCHAR (30),
        manager_name VARCHAR (30),
        manager_username VARCHAR (30),
        clients INTEGER DEFAULT 0
    )''')
except:
    logging.error('Managers table already exists.')

try:
    # creates table with information about users
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR (30),
        user_name VARCHAR (30),
        user_username VARCHAR (30),
        stocks BOOLEAN DEFAULT FALSE,
        reviews BOOLEAN DEFAULT FALSE,
        networks BOOLEAN DEFAULT FALSE,
        addresses BOOLEAN DEFAULT FALSE,
        details BOOLEAN DEFAULT FALSE,
        cost BOOLEAN DEFAULT FALSE,
        terms BOOLEAN DEFAULT FALSE,
        poizon BOOLEAN DEFAULT FALSE,
        alipay BOOLEAN DEFAULT FALSE,
        currency BOOLEAN DEFAULT FALSE,
        contract BOOLEAN DEFAULT FALSE,
        download BOOLEAN DEFAULT FALSE,
        shipment BOOLEAN DEFAULT FALSE,
        manager BOOLEAN DEFAULT FALSE,
        retarget BOOLEAN DEFAULT FALSE,
        stats BOOLEAN DEFAULT FALSE,
        actions INTEGER DEFAULT 0,
        join_date TIMESTAMP
    )''')
except Exception as ex:
    logging.error(f'Users table already exists. {ex}')

# cursor.execute("DELETE FROM managers WHERE id=4")
# database.commit()
