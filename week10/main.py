import uvicorn
from fastapi import FastAPI, WebSocket, status
import logging
from fastapi.websockets import WebSocketDisconnect

logger = logging.getLogger("uvicorn")
app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    try:
        while True:
            data = await websocket.receive_text()
            if data == "!exit":
                logger.warn("Disconnecting...")
                return await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE,
                    reason="Disconnecting as requested...",
                )
            logger.info(f"Message received: {data}")
            await websocket.send_text("Message received!")
            
    except WebSocketDisconnect:
        logger.warning("Connection closed by the client")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)