from pydantic import BaseModel, Field

class Rectangle(BaseModel):
    width: float = Field(gt=0, default=1)
    height: float = Field(gt=0, default=1)

    def area(self):
        return self.width * self.height
    
    def circumference(self):
        return 2 * self.width + 2 * self.height