from fastapi import FastAPI
import datetime
import time
import uvicorn
import asyncio

app = FastAPI()

@app.get("/sleep")
async def sleeper():
    starttime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime( time.time() ))
    await asyncio.sleep(10)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime( time.time() ))
    return "Back up from a looooong task from " + starttime + " to " + endtime

if __name__ == "__main__":
    uvicorn.run("async_demo:app", reload=True, workers=1)