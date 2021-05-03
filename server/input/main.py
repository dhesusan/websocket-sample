import asyncio
import functools

import requests
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()

clients_websocket: dict[str, WebSocket] = {}
clients_id: dict[str, str] = {}


@app.websocket("/ws/{user_id}")
async def websocket_output_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    client_id = websocket.headers.get("sec-websocket-key")
    clients_websocket[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            loop = asyncio.get_event_loop()
            func = functools.partial(
                requests.post,
                url=f"http://output-api:9099/{user_id}",
                json={"text": data},
            )
            await loop.run_in_executor(None, func)
    except WebSocketDisconnect:
        await websocket.close()
        del clients_websocket[client_id]
