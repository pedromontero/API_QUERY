"""
Main launcher for Mooring module.
Executes both plotting and excel export standalones.
"""

import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n>>> Running {script_name}...")
    try:
        # Use sys.executable to ensure we use the same Python environment
        result = subprocess.run([sys.executable, script_name], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        return False

def main():
    print("==========================================")
    print("   INTECMAR MOORING PROCESSING TOOL       ")
    print("==========================================")
    
    # Run Plots
    run_script("plots_standalone.py")
    
    # Run Excel Export
    run_script("export_standalone.py")
    
    print("\n[DONE] All Mooring tasks completed.")

if __name__ == "__main__":
    main()
