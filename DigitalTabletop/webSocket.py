import websockets
import asyncio
import json

USERS = []
MAP = {}
async def test(websocket, path):
    USERS.append(websocket)

    print(str(websocket.remote_address)+" connected")

    payload = {}
    payload["characters"] = []

    for pc in MAP:
        a = {
             "avatar":MAP[pc][2],
             "x":MAP[pc][0],
             "y":MAP[pc][1],
              "cid": pc
            }
        payload["characters"].append(a)

    await websocket.send(payload)

    try:
        while True: # while connection open...
            message = await websocket.recv()
            test = json.loads(message)
            MAP[test["cid"]] = [test["x"], test["y"], test["avatar"]]
            print("%s: %s moved to %s,%s" % (websocket.remote_address, test["cid"], test["x"], test["y"]))
            for user in USERS:
                await user.send(message)
    except websockets.exceptions.ConnectionClosed:
        USERS.remove(websocket)
START_SERVER = websockets.serve(test, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
