import os
from dotenv import load_dotenv
import psycopg2
from pymongo import MongoClient
from contextlib import contextmanager
from typing import Optional

# Load environment variables
load_dotenv()

# Global connection variables
_pg_connection = None
_mongo_client = None
_mongo_db = None

def get_pg_connection():
    """Get PostgreSQL connection (singleton pattern)"""
    global _pg_connection
    if _pg_connection is None or _pg_connection.closed:
        _pg_connection = psycopg2.connect(
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
    return _pg_connection

def get_mongo_client():
    """Get MongoDB client (singleton pattern)"""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(os.getenv("MONGO_URI"))
    return _mongo_client

def get_mongo_db():
    """Get MongoDB database"""
    global _mongo_db
    if _mongo_db is None:
        client = get_mongo_client()
        _mongo_db = client[os.getenv("MONGO_DB")]
    return _mongo_db

@contextmanager
def get_pg_cursor():
    """Context manager for PostgreSQL cursor"""
    conn = get_pg_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def get_mongo_collection(collection_name: str):
    """Get MongoDB collection"""
    db = get_mongo_db()
    return db[collection_name]

def test_pg_connection() -> bool:
    """Test PostgreSQL connection"""
    try:
        conn = get_pg_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result[0] == 1
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return False

def test_mongo_connection() -> bool:
    """Test MongoDB connection"""
    try:
        client = get_mongo_client()
        # Test connection with a simple command
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False

def close_connections():
    """Close all database connections"""
    global _pg_connection, _mongo_client, _mongo_db
    
    if _pg_connection and not _pg_connection.closed:
        _pg_connection.close()
        _pg_connection = None
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _mongo_db = None
