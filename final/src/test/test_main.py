# set the project root as src for importing modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from fastapi.testclient import TestClient
from model.item import Item, IdItem
from fake import item as service
from main import app

client = TestClient(app)

global _fake
global _fake_wo_description

def test_create_items():
	global _fake
	global _fake_wo_description
	# Using Faker library to automatically generate fake data
	f = Faker()
	item = Item(
        name=f.name(),
        description=f.text(),
        value=f.random_number(digits=5, fix_len=True) / 100  # Generate a random float value
    )
	item_wo_description = Item(
        name=f.name(),
        value=f.random_number(digits=5, fix_len=True) / 100
    )
	_fake = IdItem(**item.model_dump(), id=1)
	_fake_wo_description = IdItem(**item_wo_description.model_dump(), id=2)

	# Create an item with a description using the API
	print("Creating an item:")
	response = client.post("/items/", json=item.model_dump())
	assert response.status_code == 201
	print("\tStatus code: ", response.status_code)
	assert response.json() == _fake.model_dump()
	print("\tResponse: ", response.json())
	print()

	# Create an item without a description using the API
	print("Creating an item without a description:")
	response = client.post("/items/", json=item_wo_description.model_dump())
	assert response.status_code == 201
	print("\tStatus code: ", response.status_code)
	assert response.json() == _fake_wo_description.model_dump()
	print("\tResponse: ", response.json())
	print()

def test_create_invalid_item():
	f = Faker()
	item = {
        "description": f.text(),
        "value": f.random_number(digits=5, fix_len=True) / 100
    }

	print("Creating an item without a name:")
	response = client.post("/items/", json=item)
	assert response.status_code == 422
	print("\tStatus code: ", response.status_code)
	assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing",
                "input": item
            }
        ]
    }
	print("\tResponse: ", response.json())

def test_get_items():
	global _fake
	global _fake_wo_description

	fake_as_item = Item(
		name=_fake.name,
		description=_fake.description,
		value=_fake.value
	)
	fake_as_item_wo_description = Item(
		name=_fake_wo_description.name,
		value=_fake_wo_description.value
	)

	print("Getting first item:")
	response = client.get(f"/items/{_fake.id}")
	assert response.status_code == 200
	print("\tStatus code: ", response.status_code)
	assert response.json() == fake_as_item.model_dump()
	print("\tResponse: ", response.json())

	print("Getting second item:")
	response = client.get(f"/items/{_fake_wo_description.id}")
	assert response.status_code == 200
	print("\tStatus code: ", response.status_code)
	assert response.json() == fake_as_item_wo_description.model_dump()
	print("\tResponse: ", response.json())

def test_get_item(id, status_code = 200):
	print(f"Getting item with id {id} should have status code {status_code}:")
	response = client.get(f"/items/{id}")
	assert response.status_code == status_code
	print("\tStatus code: ", response.status_code)

test_create_items()
test_create_invalid_item()
test_get_items()
test_get_item(3, 404)
test_get_item(2)