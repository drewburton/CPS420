from fastapi import APIRouter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.rectangle import get_rectangle as service_get_rectangle

router = APIRouter(prefix='/rectangle')

@router.get('/')
def get_rectangle(width: int, height: int):
    return service_get_rectangle(width, height)