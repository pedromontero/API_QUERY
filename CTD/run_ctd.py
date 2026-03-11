"""
Author: Pedro Montero
Organization: INTECMAR
License: Open Source
"""

import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import CTDService

if __name__ == "__main__":
    service = CTDService()
    service.run()
