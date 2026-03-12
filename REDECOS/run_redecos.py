# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !                       OCXG API, CAPTA Project
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : OCXG API_QUERY
#    ! PROJECT       : CAPTA
#    ! URL           : http://observatoriocosteiro.gal/es
#    ! AFFILIATION   : INTECMAR
#    ! DATE          : March 2026
#    ! REVISION      : Montero 0.1
#    !> @author
#    !> Pedro Montero Vilar
#    !
#    ! DESCRIPTION:
#    ! Preprocessing script for collecting data from OCXG API and processing them
#    !--------------------------------------------------------------------------------------
#
#    MIT License
#
#    Copyright (c) 2026 INTECMAR
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

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
