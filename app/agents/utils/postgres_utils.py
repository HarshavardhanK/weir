import psycopg2
from psycopg2.extras import Json
import os

DATABASE_URL = os.getenv('DATABASE_URL')

def store_memory_in_db(user_id, memory_data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memories (user_id, memory_data) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET memory_data = %s",
            (user_id, Json(memory_data), Json(memory_data))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": "Memory stored successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def retrieve_memory_from_db(user_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT memory_data FROM memories WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return {"status": "success", "memory_data": result[0]}
        else:
            return {"status": "error", "message": "No memory found for user"}
    except Exception as e:
        return {"status": "error", "message": str(e)}