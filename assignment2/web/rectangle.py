from fastapi import APIRouter
import sys
import os
# work around for accessing parent directory on windows
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.rectangle import get_rectangle as service_get_rectangle

router = APIRouter(prefix='/rectangle')

@router.get('/')
def get_rectangle(width: float, height: float):
    return service_get_rectangle(width, height)

@router.get("/circumference")
def get_circumference(width: float, height: float):
    return get_rectangle(width=width, height=height).circumference()

@router.get("/area")
def get_area(width: float, height: float):
    return get_rectangle(width=width, height=height).area()