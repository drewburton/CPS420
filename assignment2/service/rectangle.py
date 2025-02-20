import sys
import os
# work around for accessing parent directory on windows
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake.rectangle import get_one

def get_rectangle(width: float, height: float):
    return get_one(width, height)