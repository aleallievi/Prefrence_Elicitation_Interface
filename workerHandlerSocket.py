import asyncio
import websockets
import numpy as np
import cv2
import mss
import mss.tools

connected = set()
seen_worker_ids = []

async def server(websocket, path):
    lastName = None
    while True:
        async for message in websocket:
            if message not in seen_worker_ids or message == "":
                seen_worker_ids.append(message)
                with open("worker_tracker.txt") as f:
                    content = f.readlines()
                sample_number = [x.strip() for x in content][0]
                print ("sending " + str(sample_number))
                await websocket.send(str(sample_number))
                sample_number = int(sample_number)
                sample_number+=1
                file = open("worker_tracker.txt","w")
                file.write(str(sample_number))
                file.close()




start_server = websockets.serve(server, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
