"""
Main launcher for REDECOS module.
Author: Pedro Montero
Organization: INTECMAR
"""

import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n>>> Running {script_name}...")
    try:
        # Use simple python interpreter, same as caller
        result = subprocess.run([sys.executable, script_name], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        return False

def main():
    print("==========================================")
    print("   INTECMAR REDECOS PROCESSING TOOL       ")
    print("==========================================")
    
    # Check config
    if not os.path.exists("input.json"):
        print("[ERR] No input.json found! Creating template...")
        template = {
            "begin_date": "2026-01-01",
            "end_date": "2026-01-05",
            "stations": ["GB", "AR", "LO"],
            "variables": ["Temperatura", "Salinidade"]
        }
        with open("input.json", "w", encoding='utf-8') as f:
            json.dump(template, f, indent=4)
        print("[OK] Skeleton input.json created. Please edit and run again.")
        return

    # 1. Run Plots
    run_script("plots_standalone.py")

    # 2. Run Export
    run_script("export_standalone.py")

    print("\n[DONE] All Redecos tasks completed.")

if __name__ == "__main__":
    main()
