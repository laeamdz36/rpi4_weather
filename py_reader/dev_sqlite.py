"""Development for connection and testing sqlite DB
    Crear un volumen persistente en un directorio local db_data
"""
import random
import sqlite3
import datetime as dt
import time


def initialize_db():

    db = ".db_data/weather.db"
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # create table
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        devicename TEXT NOT NULL,
        value REAL NOT NULL,
        timestamp TEXT NOT NULL)''')  # Cambiado a TEXT para almacenar la fecha como cadena

    conn.commit()
    conn.close()

def get_random_value() -> int:
    """Get a rando value between 0 and 100"""
    return random.randint(0,100)

def write_tstamp(db):
    """Write timestamp to sqlite DB every 3 seconds"""

    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    # get timestamp in str
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    value = get_random_value()
    c.execute(f"INSERT INTO {db} (devicename, value, timestamp) VALUES ('device_001', value, now)")
    conn.commit()

def main():
    db = ".db_data/weather.db"
    initialize_db()
    try:
        write_tstamp(db)
        time.sleep(3)
    except KeyboardInterrupt as e:
        print(e)

if __name__ == '__main__':
    main()