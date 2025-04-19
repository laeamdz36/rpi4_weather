"""Module for reading data for raspberry PI SPI interface sensor"""

import os
from time import sleep
import datetime as dt
import bme280
import smbus2
from gpiozero import CPUTemperature
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


def get_cpu_temp():
    """Reading temperature from CPU"""

    cpu = CPUTemperature()
    print(f"Current temperature: {cpu.temperature}")
    return cpu.temperature


def read_sensor():
    """Read sensor BME 280 in  76"""
    port = 1
    address = 0x76  # Adafruit BME280 address. Other BME280s may be different
    bus = smbus2.SMBus(port)

    bme280.load_calibration_params(bus, address)

    bme280_data = bme280.sample(bus, address)
    time_stamp = f"Tiempo: {bme280_data.timestamp}"
    humidity = f"Humedad actual: {bme280_data.humidity} %"
    pressure = f"Presion actual: {bme280_data.pressure} hPa"
    ambient_temperature = f"Temperatura: {bme280_data.temperature} °C"
    now = dt.datetime.today()
    head = now.strftime("%d/%m/%Y %H%M%S")
    print(head.center(50, "="))
    print(time_stamp, humidity, pressure, ambient_temperature, sep="\n")

    return {"humidity": humidity, "pressure": pressure,
            "temperature": ambient_temperature, }


def write_data(data: dict):
    """Write data into influxDB container"""

    url = os.getenv("INFLUX_URL")
    token_pth = os.getenv("INFLUX_TOKEN")
    with open(token_pth, encoding="utf-8") as f:
        token = f.read().strip()
    org = os.getenv("INFLUX_ORG")
    bucket = os.getenv("INFLUX_BUCKET")

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # write line protocol
    # measurement: weather, location = Office
    # field tags: Temperature, Pressure, Humidity
    #
    point = influxdb_client.Point("weather").tag(
        "location", "office").field(
            "temperature", data["temperature"]).tag(
            "humidity", data["humidity"]).tag(
            "pressure", data["pressure"]
    )

    write_api.write(bucket=bucket, org=org, record=point)


if __name__ == "__main__":

    while True:
        try:
            data_point = read_sensor()
            write_data(data_point)
            sleep(5)
        except Exception as e:
            print(f"Exception has occured {e.args}")
