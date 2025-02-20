from fastapi import APIRouter
from model.circle import Circle
import fake.circle as service

router = APIRouter(prefix = "/circle")

@router.get("/")
def get_all() -> list[Circle]:
    return service.get_all()

@router.get("/{radius}")
def get_one(radius) -> Circle | None:
    return service.get_one(radius)

# all the remaining endpoints do nothing yet:
@router.post("/")
def create(circle: Circle) -> Circle:
    return service.create(circle)

@router.patch("/")
def modify(circle: Circle) -> Circle:
    return service.modify(circle)

@router.put("/")
def replace(circle: Circle) -> Circle:
    return service.replace(circle)

@router.delete("/{radius}")
def delete(radius: float):
    return None