import subprocess
import sys
import time
import os

def main():
    print("Starting Agentic Email Spam Detection System...")
    
    # Path to the backend and frontend
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_script = os.path.join(base_dir, "backend", "app.py")
    frontend_script = os.path.join(base_dir, "frontend", "Home.py")

    # Start Flask Backend
    print("Starting Flask Backend...")
    backend_process = subprocess.Popen([sys.executable, backend_script])
    
    # Wait a moment to ensure backend initializes
    time.sleep(3)
    
    # Start Streamlit Frontend
    print("Starting Streamlit Frontend...")
    frontend_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", frontend_script, "--browser.gatherUsageStats", "false"])
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down system...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
