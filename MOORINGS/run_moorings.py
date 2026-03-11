"""
Standalone script to run Mooring data processing and visualization.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import MooringService

def load_config(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def main():
    print("--- Mooring Query & Visualization Tool ---")
    
    # 1. Load config
    load_dotenv()
    config = load_config('input_moorings.json')
    
    if not config:
        print("Error: input_moorings.json not found.")
        return

    # 2. Get Credentials
    url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
    user = os.getenv("API_USER")
    pwd = os.getenv("API_PASSWORD")
    
    if not user or not pwd:
        print("Error: API credentials not found in .env")
        return

    # 3. Initialize and Run
    service = MooringService(url, user, pwd)
    service.run(config)

if __name__ == "__main__":
    main()
