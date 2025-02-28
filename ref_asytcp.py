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
    """Servidor TCP asíncrono que recibe datos y los envía a WebSockets."""
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()


async def handle_client(reader, writer):
    """Maneja la comunicación con un cliente TCP y envía datos a WebSockets."""
    client_address = writer.get_extra_info('peername')
    print(f"Conexión establecida con {client_address}")

    try:
        while True:
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transmit_data = {
                "Device": "Raspberry_001",
                "STATUS": "Running",
                "current_time": now
            }
            response_json = json.dumps(transmit_data)

            # Enviar datos a WebSockets
            await send_to_websockets(response_json)

            writer.write(response_json.encode("utf-8") + b'\n')
            await writer.drain()
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        print(f"Cliente {client_address} desconectado")
    finally:
        writer.close()
        await writer.wait_closed()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Maneja conexiones WebSocket con el frontend."""
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)


async def send_to_websockets(data):
    """Envía los datos a todos los clientes WebSocket conectados."""
    if connected_clients:
        for ws in connected_clients:
            try:
                await ws.send_text(data)
            except:
                connected_clients.remove(ws)


async def start_servers():
    """Inicia el servidor TCP y el servidor web en paralelo."""
    # Crear tareas separadas para cada servidor
    # No usamos await para no bloquear el evento
    asyncio.create_task(tcp_server())
    config = uvicorn.Config(app, host=HOST, port=WEB_PORT, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start_servers())
