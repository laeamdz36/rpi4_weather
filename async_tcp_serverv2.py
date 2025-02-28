import asyncio
import json
import datetime as dt
import websockets

HOST = "0.0.0.0"
PORT = 3600


async def handle_client(reader, writer):
    """Maneja la comunicación con un cliente de forma asíncrona."""
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

            # Envía datos con delimitador
            writer.write(response_json.encode("utf-8") + b'\n')
            await writer.drain()  # Asegura que los datos se envían completamente
            print(f"Enviando respuesta a {client_address}: {response_json}")

            await asyncio.sleep(1)  # No bloquea el event loop

    except asyncio.CancelledError:
        print(f"Cliente {client_address} desconectado")
    except Exception as e:
        print(f"Error con {client_address}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    """Crea y ejecuta el servidor TCP asíncrono."""
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Servidor escuchando en {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
