from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import math
 
app = FastAPI()
 
class Triangle(BaseModel):
    side_a: float
    side_b: float
    side_c: Optional[float] = None
 
    def is_valid(self):
        sides = sorted([self.side_a, self.side_b, self.side_c] if self.side_c is not None else [self.side_a, self.side_b])
        return sides[0] + sides[1] > sides[2] if self.side_c is not None else True
 
    def calculate_hypotenuse(self):
        if self.side_c is not None:
            raise ValueError("Hypotenuse can only be calculated when it is not provided.")
        return math.sqrt(self.side_a**2 + self.side_b**2)
 
    def calculate_area(self):
        if self.side_c is None:
            return 0.5 * self.side_a * self.side_b
        else:
            s = (self.side_a + self.side_b + self.side_c) / 2
            return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
 
@app.post("/triangle/hypotenuse")
def calculate_hypotenuse(triangle: Triangle):
    if not triangle.is_valid():
        raise HTTPException(status_code=400, detail="Invalid triangle sides.")
    try:
        hypotenuse = triangle.calculate_hypotenuse()
        return {"hypotenuse": hypotenuse}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@app.post("/triangle/area")
def calculate_area(triangle: Triangle):
    if not triangle.is_valid():
        raise HTTPException(status_code=400, detail="Invalid triangle sides.")
    area = triangle.calculate_area()
    return {"area": area}
 
@app.post("/triangle/validate")
def validate_triangle(triangle: Triangle):
    return {"is_valid": triangle.is_valid()}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("triangle:app", reload=True)