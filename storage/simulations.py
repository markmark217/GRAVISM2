"""
Simulation Storage Operations
=============================
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from storage.database import get_connection


def save_simulation_record(name: str, model_type: str, config: Dict[str, Any],
                           results: Optional[Dict[str, Any]] = None) -> str:
    """
    Save a simulation configuration and optional scalar results.
    """
    sim_id = str(uuid.uuid4())[:8]
    created_at = datetime.utcnow().isoformat()

    # Clean results of large numpy arrays for metadata storage
    clean_results = {}
    if results:
        for k, v in results.items():
            if isinstance(v, (int, float, str, bool, list)):
                clean_results[k] = v

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO simulations (id, name, model_type, created_at, config_json, results_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (sim_id, name, model_type, created_at, json.dumps(config), json.dumps(clean_results)))
    conn.commit()
    conn.close()
    return sim_id


def list_saved_simulations() -> List[Dict[str, Any]]:
    """Retrieve list of saved simulations."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, model_type, created_at FROM simulations ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_simulation_by_id(sim_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve single simulation record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM simulations WHERE id = ?", (sim_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data["config"] = json.loads(data["config_json"])
        data["results"] = json.loads(data["results_json"]) if data["results_json"] else {}
        return data
    return None

