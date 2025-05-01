from pydantic import BaseModel
from typing import Optional

'''
Defines the structure of an item in the application.
'''
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    value: float

'''
Defines the structure of an item with an ID.
'''
class IdItem(Item):
    id: int