import asyncio
import websockets
import json
import random
import pandas as pd
import time

# Load your real past data into a DataFrame (replace this with actual file)
data = {
    'timestamp': pd.date_range(start='2022-01-01', periods=100, freq='D'),
    'open': [100 + random.randint(-5, 5) for _ in range(100)],
    'high': [105 + random.randint(-5, 5) for _ in range(100)],
    'low': [95 + random.randint(-5, 5) for _ in range(100)],
    'close': [100 + random.randint(-5, 5) for _ in range(100)]
}
df = pd.DataFrame(data)


async def price_stream(websocket, path):
    for index, row in df.iterrows():
        # Create JSON object to send to the client
        price_data = {
            "timestamp": str(row['timestamp']),
            "open": row['open'],
            "high": row['high'],
            "low": row['low'],
            "close": row['close']
        }

        # Send the JSON object to the client
        await websocket.send(json.dumps(price_data))

        # Wait for 1 second before sending the next data point
        await asyncio.sleep(1)


# Set up the WebSocket server
start_server = websockets.serve(price_stream, "localhost", 8080)

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
