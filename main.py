# main.py
import subprocess, os, sys

# Path to the demo entry point
demo_path = os.path.join(os.path.dirname(__file__), "demo", "demo_mainLoginScreen.py")

# Run the demo script with the same Python interpreter
subprocess.run([sys.executable, demo_path])