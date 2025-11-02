
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import os, json
import sqlite3

app = FastAPI(title="Task 3 API")

DB_PATH = "predictions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            prediction TEXT,
            probability TEXT,
            predicted_at TEXT,
            inputs_json TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class PredictionLog(BaseModel):
    record_id: Optional[str] = None
    prediction: Any
    probability: Any = None
    predicted_at: str
    inputs: Dict[str, Any]

def latest_from_dataset():
    for name in os.listdir("data"):
        if name.lower().endswith(".csv"):
            import pandas as pd
            df = pd.read_csv(os.path.join("data", name))
            if not df.empty:
                return df.tail(1).to_dict(orient="records")[0]
    return None

@app.get("/api/records/latest")
def get_latest():
    row = latest_from_dataset()
    if row is None:
        # DEFAULT IS NUMERIC to match the dummy model
        row = {"id": 1, "feature_1": 3.5, "feature_2": 2.8, "feature_3": 0.0}
    return row

@app.post("/api/predictions")
def log_prediction(payload: PredictionLog = Body(...)):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO prediction_logs (record_id, prediction, probability, predicted_at, inputs_json, created_at) VALUES (?,?,?,?,?,?)",
        (
            str(payload.record_id) if payload.record_id is not None else None,
            json.dumps(payload.prediction),
            json.dumps(payload.probability),
            payload.predicted_at,
            json.dumps(payload.inputs),
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "logged": True}
