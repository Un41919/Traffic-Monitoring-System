"""
=========================================
SQLite Database Manager
Traffic-Monitoring-System
Version : 1.0.0
=========================================
"""

import sqlite3
import os

from datetime import datetime


# ==================================================
# Database Path
# ==================================================

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "traffic.db"
)


# ==================================================
# Database Class
# ==================================================

class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH
        )

        self.cursor = self.connection.cursor()

        print("=" * 50)
        print("SQLite Connected")
        print("=" * 50)
        print(f"Database : {DATABASE_PATH}")

    # ==================================================
    # Insert Vehicle
    # ==================================================

    def insert_vehicle(

        self,

        camera,

        track_id,

        vehicle_type,

        direction,

        confidence

    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(

            """
            INSERT INTO vehicle_detection (

                timestamp,

                camera,

                track_id,

                vehicle_type,

                direction,

                confidence

            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,

            (

                timestamp,

                camera,

                track_id,

                vehicle_type,

                direction,

                confidence

            )

        )

        self.connection.commit()

    # ==================================================
    # Close
    # ==================================================

    def close(self):

        self.connection.close()

        print("SQLite Closed")