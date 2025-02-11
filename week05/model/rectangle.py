from pydantic import BaseModel, Field

class Rectangle(BaseModel):
    width: float = Field(gt=0, default=1)
    height: float = Field(gt=0, default=1)