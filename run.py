"""
Campus Placement Management System — Entry Point
Run this file to start the application: python run.py
"""

import sys
import os
import webbrowser
import threading

# Change to backend directory so imports work
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from database import init_db
from app import create_app


def open_browser():
    import time
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    print("=" * 60)
    print("  Campus Placement Management System")
    print("=" * 60)
    init_db()
    app = create_app()
    threading.Thread(target=open_browser, daemon=True).start()
    print("\n  Server: http://localhost:5000")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=False, port=5000, host='0.0.0.0')
