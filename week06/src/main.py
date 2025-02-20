import uvicorn
from fastapi import FastAPI
from web import circle

app = FastAPI()

app.include_router(circle.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)