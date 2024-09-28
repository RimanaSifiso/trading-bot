import asyncio
import websockets


async def receive_price_data():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        while True:
            # Receive data from server
            data = await websocket.recv()
            print(f"Received: {data}")


# Run the client
asyncio.get_event_loop().run_until_complete(receive_price_data())
