"""Build a TCP server SOCKET to coomunicate and sen json data"""

import socket
import json
import time
import datetime as dt

HOST = "0.0.0.0"
PORT = 3600

# Crear un purto TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    print(f"Servidor escuchando en {HOST}, {PORT}")
    server.listen(2)

    while True:
        # Acpetar conexion entrante
        client_socket, client_address = server.accept()
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transmit_data = {
            "Device": "Raspberry_001",
            "STATUS": "Running",
            "current_time": now
        }
        while True:
            try:

                print(f"Conexion establecida con {client_address}")

                # Send data over TCP socket
                response_json = json.dumps(transmit_data)
                client_socket.sendall(response_json.encode("utf-8"))
                print(f"enviando respuesta {response_json}")
                time.sleep(5)
            except ConnectionResetError:
                break

        client_socket.close()
