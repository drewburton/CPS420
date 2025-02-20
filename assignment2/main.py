from fastapi import FastAPI
from web.rectangle import router

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)