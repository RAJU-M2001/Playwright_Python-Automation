import subprocess
import os

resume_path = os.path.join(os.path.dirname(__file__), "Resume.py")
subprocess.run(["python", resume_path])