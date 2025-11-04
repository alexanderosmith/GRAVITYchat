#!/usr/bin/env python3
"""
GRAVITYchat - Startup Script
-----------------------------
Simple script to run the RAG chatbot with mock data for demonstration.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the app
from app.main import app
import uvicorn

def main():
    """Run the GRAVITYchat application."""
    print("🚀 Starting GRAVITYchat RAG System...")
    print("📚 LIGO/Gravity Spy Citizen Science Chatbot")
    print("🔬 Powered by FastAPI (Local Testing Mode)")
    print("=" * 50)
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    # Run with mock settings for demonstration
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid warnings
        log_level="info"
    )

if __name__ == "__main__":
    main()

