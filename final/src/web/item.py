from fastapi import APIRouter, HTTPException
from model.item import Item, IdItem
import fake.item as service

router = APIRouter(prefix = "/items")

'''
Endpoint to retrieve one item by id
:param id: The id of the item to retrieve
:return: The item with the given id (200)
:raises HTTPException: If the item is not found (404)
'''
@router.get("/{id}")
def get_one(id: int) -> Item | None:
	item = service.get_one(id)
	if item is None:
		raise HTTPException(status_code=404, detail="No items found")
	return item

'''
Endpoint to create an item
:param item: The item to create
:return: The created item (201)
'''
@router.post("/", status_code=201)
def create(item: Item) -> IdItem:
    return service.create(item)