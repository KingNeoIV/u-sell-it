# main.py
import subprocess, os, sys, platform

# Detect the operating system
system = platform.system().lower()  # "windows", "linux", "darwin" (macOS)

# Map OS to the correct demo script
if system == "linux":
    demo_path = os.path.join(os.path.dirname(__file__), "linuxDemo", "linuxDemo_mainLoginScreen.py")
elif system == "windows":
    demo_path = os.path.join(os.path.dirname(__file__), "demo", "demo_mainLoginScreen.py")
elif system == "darwin":  # macOS
    print("macOS demo coming soon!")
    sys.exit(0)  # exit gracefully without trying to run a demo
else:
    print(f"{system.capitalize()} not supported yet.")
    sys.exit(0)

# Run the demo script with the same Python interpreter
subprocess.run([sys.executable, demo_path])
