from fastapi import FastAPI, Body, Request
from fastapi.responses import RedirectResponse, FileResponse
import starlette.status as status

app = FastAPI()

# default
@app.get("/hi")
def greet():
    return "Hello? World?"

# URL path
@app.get("/hi2/{name}")
def greet2(name: str):
    return f"Hello? {name}?"

# Query parameters
@app.get("/hi3")
def greet3(name: str):
    return f"Hello? {name}?"

# POST
@app.post("/hi4")
def greet4(name:str = Body(embed=True)):
    return f"Hello? {name}?"

# Redirect
@app.get("/not/here")
def redirect():
    return RedirectResponse(url="https://cnets-teach.gitlab.io/cmich-cps-420/", status_code=status.HTTP_301_MOVED_PERMANENTLY)

# file
import os
@app.get("/gimme")
def get_file():
    return FileResponse(path=os.path.basename(__file__), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("example_3_1:app", reload=True, port=4000)