import asyncio
import websockets
import requests

SERVER_URL = "http://127.0.0.1:8000"


# -------------------------------
# Register User
# -------------------------------
def register():
    print("\n--- Register New User ---")
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    response = requests.post(
        f"{SERVER_URL}/register",
        json={"username": username, "password": password}
    )

    print("Server Response:", response.json())


# -------------------------------
# Login User
# -------------------------------
def login():
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")

    response = requests.post(
        f"{SERVER_URL}/login",
        json={"username": username, "password": password}
    )

    if response.status_code != 200:
        print("❌ Login Failed:", response.json())
        return None

    token = response.json()["token"]
    print("✅ Login Successful!")
    return token


# -------------------------------
# Chat Client WebSocket
# -------------------------------
async def chat_client(token):

    ws_url = f"ws://127.0.0.1:8000/ws?token={token}"

    async with websockets.connect(ws_url) as websocket:

        print("\n✅ Connected to Chatterbox Chat Room!")
        print("Type messages and press Enter...")
        print("Type /quit to exit.\n")

        # -------------------------------
        # Receive Messages Task
        # -------------------------------
        async def receive_messages():
            while True:
                try:
                    msg = await websocket.recv()
                    print(msg)
                except:
                    print("\n❌ Disconnected from server")
                    break

        # -------------------------------
        # Send Messages Task (FIXED)
        # -------------------------------
        async def send_messages():
            while True:
                try:
                    # ✅ FIX: Non-blocking input
                    message = await asyncio.to_thread(input)

                    if message.lower() == "/quit":
                        print("👋 Leaving chat...")
                        break

                    await websocket.send(message)

                except:
                    break

        # Run both tasks together
        await asyncio.gather(receive_messages(), send_messages())


# -------------------------------
# Main Menu
# -------------------------------
def main():
    print("\n==============================")
    print("   💬 CHATTERBOX CLIENT")
    print("==============================")

    while True:
        print("\n1. Register")
        print("2. Login & Join Chat")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            register()

        elif choice == "2":
            token = login()
            if token:
                asyncio.run(chat_client(token))

        elif choice == "3":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()
