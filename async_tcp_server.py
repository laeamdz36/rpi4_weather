"""TCP server asynchronous"""
import asyncio
import json
import datetime as dt

HOST = "0.0.0.0"
PORT = 3600


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión establecida con {addr}")

    try:
        while True:
            # Leer datos del cliente (si es necesario)
            data = await reader.read(100)  # Lee hasta 100 bytes
            if not data:
                break  # Si no hay datos, salir del bucle

            # Procesar los datos recibidos (opcional)
            print(f"Recibido: {data.decode()} de {addr}")

            # Preparar la respuesta
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transmit_data = {
                "Device": "Raspberry_001",
                "STATUS": "Running",
                "current_time": now
            }
            response_json = json.dumps(transmit_data)

            # Enviar la respuesta al cliente
            writer.write(response_json.encode("utf-8"))
            await writer.drain()  # Esperar a que los datos se envíen
            print(f"Enviando respuesta {response_json} a {addr}")

    except ConnectionResetError:
        print(f"Conexión con {addr} reseteada")
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        # Cerrar la conexión
        writer.close()
        await writer.wait_closed()
        print(f"Conexión cerrada con {addr}")


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Servidor escuchando en {HOST}, {PORT}")

    async with server:
        await server.serve_forever()  # Mantener el servidor activo indefinidamente

# Ejecutar el servidor
asyncio.run(main())
