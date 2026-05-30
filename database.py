# database.py
# Part c) - Integrate event driven database to the application software

import sqlite3
from datetime import datetime

class RobotDatabase:
    """
    Every time the robot does something (move, pick, place),
    this class automatically saves it to a database as an 'event'.
    That's what 'event-driven' means!
    """

    def __init__(self, db_name="robot_events.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        print(f"[DATABASE] Connected to {self.db_name}")

    def _create_table(self):
        """Create the events table if it doesn't exist yet"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS robot_events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT NOT NULL,
                event_type  TEXT NOT NULL,
                details     TEXT NOT NULL,
                position    TEXT NOT NULL,
                status      TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def log_event(self, event_type, details, position, status):
        """Save a robot event to the database"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO robot_events 
            (timestamp, event_type, details, position, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, event_type, details, str(position), status))
        self.connection.commit()
        print(f"[DATABASE] Event logged: {event_type} - {details}")

    def get_all_events(self):
        """Retrieve all events from the database"""
        self.cursor.execute(
            "SELECT * FROM robot_events ORDER BY id DESC"
        )
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection"""
        self.connection.close()
        print("[DATABASE] Connection closed.")