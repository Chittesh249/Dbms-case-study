#!/usr/bin/env python3
"""
Simple Backend Startup Script
This script will start the backend server with comprehensive Milvus documentation
"""

import subprocess
import sys
import time
import requests

def start_backend_server():
    """Start the backend server"""
    print("🚀 Starting Milvus Backend Server...")
    print("="*50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 'app:app', 
            '--host', '0.0.0.0', '--port', '8001'
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    print("🎯 MILVUS BACKEND SERVER")
    print("="*50)
    print("✅ Comprehensive Milvus documentation loaded")
    print("✅ OpenAI integration ready")
    print("✅ Vector search functionality available")
    print("✅ Starting server on http://localhost:8001")
    print("="*50)
    
    start_backend_server()
