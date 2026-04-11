import sys
import subprocess
import os
import glob

DEPS = ["zstd", "mercury-engine-data-structures", "construct", "jsonschema", "ips.py", "open-dread-rando-exlaunch"]

def run_pip(python_exe):
    print(f"Found Python at: {python_exe}")
    print(f"Installing: {', '.join(DEPS)}")
    
    cmd = [python_exe, "-m", "pip", "install"] + DEPS
    
    try:
        subprocess.check_call(cmd)
        print("\nSUCCESS: Dependencies installed for this Python environment.")
    except subprocess.CalledProcessError:
        print("\nDetected externally managed environment. Retrying with --break-system-packages...")
        try:
            subprocess.check_call(cmd + ["--break-system-packages"])
            print("\nSUCCESS: Dependencies installed using --break-system-packages.")
        except Exception as e:
            print(f"\nERROR: Failed to install dependencies: {e}")
            print("\nIf you are running Archipelago from source, please activate your virtual environment first.")
            print("If you are using the Archipelago app, please ensure you are using the internal Python.")
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")

def main():
    print("Metroid Dread AP Dependency Installer")
    print("--------------------------------------")
    
    # Common locations for Archipelago Python on Mac
    mac_paths = [
        "/Applications/Archipelago.app/Contents/Resources/app/python3",
        "/Applications/Archipelago-0.6.7.app/Contents/MacOS/Archipelago.app/Contents/Resources/app/python3",
        sys.executable # Current python
    ]
    
    found_any = False
    for path in mac_paths:
        if os.path.exists(path):
            run_pip(path)
            found_any = True
            break
            
    if not found_any:
        print("\nCOULD NOT AUTOMATICALLY FIND ARCHIPELAGO PYTHON.")
        print("Please run this script manually using the Python executable within your Archipelago installation.")
        print("Example: /Applications/Archipelago.app/Contents/Resources/app/python3 install_deps.py")

if __name__ == "__main__":
    main()
