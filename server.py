from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from manager import ConnectionManager
import database

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
manager = ConnectionManager()
database.init_db()

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    success = database.register_user(user.username, user.password)
    if success:
        return {"message": "User registered successfully"}
    return {"error": "Username already exists"}

@app.post("/login")
def login(user: User):
    if database.login_user(user.username, user.password):
        return {"message": "Login successful"}
    return {"error": "Invalid credentials"}
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            # This waits for a message from the user
            data = await websocket.receive_text()
            # This sends the message to everyone else
            await manager.broadcast(f"User {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {client_id} left the chat")

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)

    # Send chat history
    for msg in database.get_recent_messages():
        await websocket.send_text(f"{msg[0]} [{msg[2]}]: {msg[1]}")

    try:
        while True:
            data = await websocket.receive_text()
            database.save_message(username, data)
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat")