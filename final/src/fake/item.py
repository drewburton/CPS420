from model.item import Item, IdItem

# In-memory storage for items with an id counter
_id_counter = 0
_items = {}

'''
Get an item by id
:param id: The id of the item to get
:return: The item, or None if not found
'''
def get_one(id: int) -> Item | None:
	if id not in _items:
		return None
	return _items[id]

'''
Create a new item
:param item: The item to create
:return: The created item with its id
'''
def create(item: Item) -> IdItem:
	global _id_counter
	_id_counter += 1
	_items[_id_counter] = item
	return IdItem(**item.dict(), id=_id_counter)