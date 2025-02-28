# Docker file to execute aplication for sensor reading from BME280
FROM python:3.13.1-alpine3.21
WORKDIR /app
# COPY requirements.txt /app
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn websockets
COPY . /app
ENV RUNMODE=prod
EXPOSE 3600 8000
# CMD ["python", "weather_opc.py"]
# CMD ["python", "tcp_server.py"]
# CMD ["python", "async_tcp_server.py"]
CMD ["python", "ref_asytcp.py"]
# 3600:3600
# left host port : right container port
# docker run -d -p 3700:3700 nombre_de_la_imagen