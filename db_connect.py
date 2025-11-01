import os
from dotenv import load_dotenv
import psycopg2
from pymongo import MongoClient

# Load credentials
load_dotenv()

# PostgreSQL
pg_conn = psycopg2.connect(
    dbname=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT")
)
print("Connected to PostgreSQL!")

# MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("MONGO_DB")]
print("Connected to MongoDB!")

# Example test query
cursor = pg_conn.cursor()
cursor.execute("SELECT COUNT(*) FROM customers;")
print("Customers in PostgreSQL:", cursor.fetchone()[0])

print("Documents in Mongo customers:", mongo_db.customers.count_documents({}))
