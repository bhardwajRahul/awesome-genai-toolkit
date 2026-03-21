import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "podcastbrain.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            summary TEXT,
            key_takeaways TEXT,
            segments_json TEXT NOT NULL,
            rating INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# --- Episodes ---

def save_episode(topic: str, summary: str, key_takeaways: list[str], segments: list[dict]) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO episodes (topic, summary, key_takeaways, segments_json) VALUES (?, ?, ?, ?)",
        (topic, summary, json.dumps(key_takeaways), json.dumps(segments)),
    )
    conn.commit()
    episode_id = c.lastrowid
    conn.close()
    return episode_id


def get_episode(episode_id: int) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM episodes WHERE id = ?", (episode_id,)).fetchone()
    conn.close()
    if not row:
        return None
    ep = dict(row)
    ep["segments"] = json.loads(ep["segments_json"])
    ep["key_takeaways"] = json.loads(ep["key_takeaways"]) if ep["key_takeaways"] else []
    return ep


def get_all_episodes() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM episodes ORDER BY created_at DESC").fetchall()
    conn.close()
    episodes = []
    for row in rows:
        ep = dict(row)
        ep["segments"] = json.loads(ep["segments_json"])
        ep["key_takeaways"] = json.loads(ep["key_takeaways"]) if ep["key_takeaways"] else []
        episodes.append(ep)
    return episodes


def rate_episode(episode_id: int, rating: int):
    conn = get_connection()
    conn.execute("UPDATE episodes SET rating = ? WHERE id = ?", (rating, episode_id))
    conn.commit()
    conn.close()


# --- User Preferences ---

def get_preference(key: str, default: str = "") -> str:
    conn = get_connection()
    row = conn.execute("SELECT value FROM user_preferences WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_preference(key: str, value: str):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO user_preferences (key, value, updated_at) VALUES (?, ?, ?)",
        (key, value, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_all_preferences() -> dict:
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM user_preferences").fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}


def get_liked_topics() -> list[str]:
    raw = get_preference("liked_topics", "[]")
    return json.loads(raw)


def add_liked_topic(topic: str):
    topics = get_liked_topics()
    if topic not in topics:
        topics.append(topic)
        set_preference("liked_topics", json.dumps(topics))


def get_past_topics() -> list[str]:
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT topic FROM episodes ORDER BY created_at DESC LIMIT 20").fetchall()
    conn.close()
    return [row["topic"] for row in rows]


# Initialize on import
init_db()
