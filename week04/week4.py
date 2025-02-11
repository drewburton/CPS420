from pydantic import BaseModel, Field, ValidationError, validator
from fastapi import FastAPI

class Rectangle(BaseModel):
    width: float = Field(gt=0, default=1)
    height: float = Field(gt=0, default=1)

    @validator('width')
    def testing_lgt(cls, value):
        if ():
            raise ValueError("HAL does not like this.")

app = FastAPI()

@app.post("/rect")
def creat_rect(rect: Rectangle, status_code=201):
    try:
        return rect
    except ValidationError as e:
        return ""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("week4:app", reload=True)