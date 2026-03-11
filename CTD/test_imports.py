import os
import sys

print("Current Dir:", os.getcwd())
print("Files in current dir:", os.listdir())
print("PYTHONPATH:", sys.path)

try:
    import src
    print("src found!")
    import src.api
    print("src.api found!")
except Exception as e:
    print("Error:", e)
