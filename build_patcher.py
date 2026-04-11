import os
import subprocess
import sys
import platform
import shutil
from pathlib import Path

def build():
    print("Building Metroid Dread Randomizer Patcher Standalone...")
    
    # Project root
    root = Path(__file__).parent.absolute()
    os.chdir(root)
    
    # Source entry point
    entry_point = root / "src" / "open_dread_rando" / "gui.py"
    
    # Data files to include
    # Format: "source_path:dest_path" (on Windows) or "source_path;dest_path" (on POSIX)
    # PyInstaller uses : as separator on POSIX and ; on Windows
    sep = os.pathsep
    data_dir = root / "src" / "open_dread_rando" / "files"
    add_data = f"{data_dir}{sep}open_dread_rando/files"
    
    # Run PyInstaller using the current Python executable
    python_exe = sys.executable
    if sys.platform == "darwin" and "homebrew" not in python_exe.lower() and os.path.exists("/opt/homebrew/opt/python@3.12/bin/python3.12"):
        # Fallback for Mac users who accidentally run the script with system python
        python_exe = "/opt/homebrew/opt/python@3.12/bin/python3.12"

    cmd = [
        python_exe, "-m", "PyInstaller",
        "--onefile",
        "--windowed", # No console on startup
        "--name", "MetroidDreadPatcher",
        "--paths", "src",  # Tell PyInstaller to look in the src directory
        "--collect-data", "mercury_engine_data_structures",
        "--collect-submodules", "mercury_engine_data_structures",
        "--hidden-import", "json_delta",
        "--collect-data", "construct",
        "--collect-submodules", "construct",
        "--collect-data", "open_dread_rando_exlaunch",
        "--collect-submodules", "open_dread_rando_exlaunch",
        "--add-data", add_data,
        str(entry_point)
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\nSUCCESS: Executable created in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: PyInstaller failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    build()
