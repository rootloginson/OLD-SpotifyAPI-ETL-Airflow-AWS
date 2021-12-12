import sqlite3
from datetime import datetime


def update_db(track_details: dict, date_time: datetime) -> None:
    conn = sqlite3.connect('track_request_history.sql')
    cur = conn.cursor()

    sql_db_create = """
    CREATE TABLE IF NOT EXISTS Random_Tracks(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            date_time TEXT,
            artist_name TEXT,
            album_name TEXT,
            track_name TEXT,
            track_external_url TEXT,
            track_uri TEXT
    )
    """
    cur.execute(sql_db_create)

    if track_details:
        sql_update_db = """
        INSERT INTO Random_Tracks
        (date_time, artist_name, album_name, track_name, track_external_url, track_uri)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            date_time,
            track_details['artist_name'],
            track_details['album_name'],
            track_details['track_name'],
            track_details['track_external_urls'],
            track_details['track_uri']
            )
        cur.execute(sql_update_db, values)

    conn.commit()
    conn.close()
