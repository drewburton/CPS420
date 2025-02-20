from .init import conn, curs
from model.circle import Circle

curs.execute("""create table if not exists circle(
 radius text primary key
 )""")

def row_to_model(row: tuple) -> Circle:
 radius, = row
 return Circle(radius=radius)

def model_to_dict(circle: Circle) -> dict:
 return circle.dict()

def get_one(radius: float) -> Circle:
 qry = "select * from circle where radius=:radius"
 params = {"radius": radius}
 curs.execute(qry, params)
 return row_to_model(curs.fetchone())

def get_all() -> list[Circle]:
 qry = "select * from circle"
 curs.execute(qry)
 return [row_to_model(row) for row in curs.fetchall()]

def create(circle: Circle) -> Circle:
 qry = "insert into circle values(:radius)"
 params = model_to_dict(circle)
 curs.execute(qry, params)
 return get_one(circle.radius)

def modify(circle: Circle, new_circle: Circle) -> Circle:
 qry = """update circle
 set radius=:radius
 where radius=:radius_org"""
 params = model_to_dict(new_circle)
 params["radius_org"] = circle.radius
 _ = curs.execute(qry, params)
 return get_one(circle.radius)

def delete(circle: Circle) -> bool:
 qry = "delete from circle where radius = :radius"
 params = {"radius": circle.radius}
 res = curs.execute(qry, params)
 return bool(res) 