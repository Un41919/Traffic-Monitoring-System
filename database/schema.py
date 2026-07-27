"""
=========================================
SQLite Database Schema
Traffic-Monitoring-System
Version : 1.0.0
=========================================
"""

import sqlite3
import os


# ==================================================
# Database Path
# ==================================================

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "traffic.db"
)


# ==================================================
# Create Database
# ==================================================

def create_database():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS vehicle_detection (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            camera TEXT NOT NULL,

            track_id INTEGER NOT NULL,

            vehicle_type TEXT NOT NULL,

            direction TEXT NOT NULL,

            confidence REAL NOT NULL

        )

    """)

    conn.commit()

    conn.close()

    print("=" * 50)
    print("SQLite Database Initialized")
    print("=" * 50)
    print(f"Database : {DATABASE_PATH}")
    print("Table    : vehicle_detection")