from asyncio import Queue
from typing import NamedTuple

from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class Data(BaseModel):
    text: str


class UserData(NamedTuple):
    user_id: str
    data: Data


app = FastAPI()
queue: Queue[UserData] = Queue()

clients_websocket: dict[str, WebSocket] = {}
clients_id: dict[str, str] = {}


@app.websocket("/ws/{user_id}")
async def websocket_output_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    client_id = websocket.headers.get("sec-websocket-key")
    clients_id[user_id] = client_id
    clients_websocket[client_id] = websocket
    try:
        while True:
            user_data = await queue.get()
            client = clients_websocket[clients_id[user_data.user_id]]
            await client.send_text(
                f"Output: ID: {user_data.user_id} | Message: {user_data.data.text}"
            )
    except WebSocketDisconnect:
        await websocket.close()
        del clients_websocket[client_id]
        del client_id[user_id]


@app.post("/{user_id}")
async def post_data(user_id: str, data: Data):
    queue.put_nowait(UserData(user_id=user_id, data=data))
