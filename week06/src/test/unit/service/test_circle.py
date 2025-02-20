from model.circle import Circle
from service import creature as code

sample = Circle(radius=)
def test_create():
 resp = code.create(sample)
 assert resp == sample
def test_get_exists():
 resp = code.get_one("yeti")
 assert resp == sample
def test_get_missing():
 resp = code.get_one("boxturtle")
 assert data is None
