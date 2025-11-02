#!/usr/bin/env python3
"""
Database Prediction Pipeline - Main Application Entry Point
"""

import sys
import os
import uvicorn

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.main import app

def main():
    """Main application entry point"""
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    # For direct execution
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
