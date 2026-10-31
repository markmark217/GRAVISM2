"""
Local Storage and SQLite Database
=================================

Persistent storage for simulations, user experiments, and scientific results.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "gravisim.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        model_type TEXT NOT NULL,
        created_at TEXT NOT NULL,
        config_json TEXT NOT NULL,
        results_json TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        hypothesis TEXT,
        simulation_id TEXT,
        observations TEXT,
        interpretation TEXT,
        conclusion TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# Ensure database initializes when module is imported
init_db()

