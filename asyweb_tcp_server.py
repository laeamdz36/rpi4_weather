"""Module for running an asynchornous TCP server with web intergface"""

import asyncio
import json
import datetime as dt
import websockets
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import uvicorn

HOST = "0.0.0.0"
PORT = 3600
WEB_PORT = 8000
connected_clients = set()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


async def tcp_server():
    """Servidor TCP async for receive and send data to websockets"""
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()


async def handle_client(reader, writer):
    """Handle connection with a TCP client and sen data to websockets"""

    client_address = writer.get_extra_info("peername")
    print(f"Stablished connection {client_address}")

    try:
        while True:
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transmit_data = {
                "Device": "Raspberry_001",
                "STATUS": "Running",
                "current_time": now
            }
            response_json = json.dumps(transmit_data)
            # send data to websocket
            await send_to_websockets(response_json)

            writer.write(response_json.encode("utf-8") + b"\n")
            await writer.drain()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"Client {client_address} desconected")
    finally:
        writer.close()
        await writer.close()
        await writer.await_closed()


@app.websocket("/ws")
async def web_socket_endpoint(websocket: WebSocket):
    """Handle conections WebSocket with frontend"""

    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # maintain conection open
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error as {e}")
    finally:
        connected_clients.remove(websocket)


async def send_to_websockets(data):
    """Send data to all websocket clients connected"""

    if connected_clients:
        for ws in connected_clients:
            try:
                await ws.send_text(data)
            except:
                connected_clients.remove(ws)


async def main():
    """Execute server TCP and web server"""

    await asyncio.gather(tcp_server(), uvicorn.run(app, host=HOST, port=WEB_PORT))

if __name__ == "__main__":
    asyncio.run(main())
