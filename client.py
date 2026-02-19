import asyncio
import websockets
import sys

async def chat(username):
    uri = f"ws://localhost:8000/ws/{username}"
    async with websockets.connect(uri) as websocket:

        async def send():
            while True:
                message = input()
                await websocket.send(message)

        async def receive():
            while True:
                msg = await websocket.recv()
                print(msg)

        await asyncio.gather(send(), receive())

if __name__ == "__main__":
    username = input("Enter your username: ")
    asyncio.run(chat(username))