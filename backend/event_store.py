import sqlite3

DB_PATH = "data/naitra.db"


def create_database():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        camera_id TEXT,
        location TEXT,
        timestamp REAL,
        confidence REAL,
        video_path TEXT,
        UNIQUE(person_id, camera_id, timestamp)
    )
""")

    connection.commit()
    connection.close()


def save_event(event):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO events
    (person_id, camera_id, location, timestamp, confidence, video_path)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    event["person_id"],
    event["camera_id"],
    event["location"],
    event["timestamp"],
    event["confidence"],
    event["video_path"]
))

    connection.commit()
    connection.close()