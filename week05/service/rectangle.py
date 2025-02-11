import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake.rectangle import get_one

def get_rectangle(width: int, height: int):
    return get_one(width, height)