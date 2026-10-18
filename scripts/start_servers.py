"""
Dron-AI Server Launcher

Runs both the Flask REST API backend and the Frontend static HTTP server concurrently.
Automatically opens the dashboard in your default browser.
"""

import subprocess
import sys
import time
import webbrowser


def main():
    print("\n==============================================================")
    print("       🚀 Launching Dron-AI Career Guidance Platform          ")
    print("==============================================================")

    # 1. Start Flask REST API Backend on port 5000
    print("[1/2] Starting Flask Backend API on http://localhost:5000 ...")
    backend = subprocess.Popen([sys.executable, "run.py"])

    # 2. Start Frontend Static HTTP Server on port 8000 (bind 127.0.0.1)
    print("[2/2] Starting Frontend Web Server on http://localhost:8000 ...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000", "--bind", "127.0.0.1"],
        cwd="frontend",
    )

    # Allow servers a brief moment to initialize
    time.sleep(1.5)

    print("\n==============================================================")
    print("       ✅ Both Servers Are Live & Ready!                     ")
    print("==============================================================")
    print("   🌐 Web Dashboard: http://localhost:8000")
    print("      (Direct link:  http://localhost:8000/html/index.html)")
    print("   ⚙️  Backend API:   http://localhost:5000/api/health")
    print("==============================================================")
    print("   Press Ctrl+C in this terminal anytime to stop both servers.\n")

    # Automatically open the dashboard in the user's default browser
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers gracefully...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("All servers stopped successfully.")


if __name__ == "__main__":
    main()

