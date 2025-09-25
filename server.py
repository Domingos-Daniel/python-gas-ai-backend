#!/usr/bin/env python3
"""
Server entry point for Leapcell deployment.
This file serves as the main entry point when deploying to Leapcell.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the FastAPI app from the app module
from app.main import app
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Leapcell sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )