import uvicorn
from fastapi import FastAPI
from web import item

app = FastAPI()

app.include_router(item.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)