# No changes needed in app2.py for this modification.
# It remains the same as in the previous example.

import uvicorn
from fastapi import FastAPI
import datetime

app = FastAPI(title="App 2 - Provider")

@app.get("/")
async def read_root_app2():
    """Provides basic info about App 2."""
    return {"message": "Hello from App 2 (Provider). Call /provide-data to get information."}

@app.get("/provide-data")
async def provide_some_data():
    """Provides some example data."""
    print("App 2 received a request for /provide-data")
    return {
        "source": "App 2",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "payload": {"item_id": 123, "status": "active"}
    }

if __name__ == "__main__":
    print("Starting App 2 on http://0.0.0.0:14124")
    uvicorn.run("app2:app", host="0.0.0.0", port=14124, reload=True)