import websockets
import asyncio
import json

USERS = []

async def test(websocket, path):
    USERS.append(websocket)
    print("%s connected" % websocket.remote_address)
    try:
        while True: # while connection open...
            message = await websocket.recv()
            test = json.loads(message)
            print("%s: %s moved to %s,%s" % (websocket.remote_address, test["cid"], test["x"], test["y"]))
            for user in USERS:
                await user["websocket"].send(message)
    except websockets.exceptions.ConnectionClosed:
        USERS.remove(websocket)
START_SERVER = websockets.serve(test, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
