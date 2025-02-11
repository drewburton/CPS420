import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.rectangle import Rectangle

_rectangles = [
    Rectangle(width=2, height=5),
    Rectangle(width=7, height=3),
    Rectangle(width=4, height=4)
]

def get_all() -> list[Rectangle]:
    """Return all explorers"""
    return _rectangles

def get_one(width: int, height: int) -> Rectangle | None:
    for _rectangle in _rectangles:
        if _rectangle.width == width and _rectangle.height == height:
            return _rectangle
    return None