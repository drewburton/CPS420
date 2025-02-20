from model.circle import Circle
import fake.circle as data

def get_all() -> list[Circle]:
    return data.get_all()

def get_one(name: str) -> Circle | None:
    return data.get(id)

def create(circle: Circle) -> Circle:
    return data.create(circle)

def replace(id, circle: Circle) -> Circle:
   return data.replace(id, circle)

def modify(id, circle: Circle) -> Circle:
    return data.modify(id, circle)

def delete(id, circle: Circle) -> bool:
    return data.delete(id)
