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
    return round(float(cpu.temperature), 2)


def read_sensor():
    """Read sensor BME 280 in  76"""
    port = 1
    address = 0x76  # Adafruit BME280 address. Other BME280s may be different
    bus = smbus2.SMBus(port)

    bme280.load_calibration_params(bus, address)
    bme280_data = bme280.sample(bus, address)
    # data asignation
    temperature = round(float(bme280_data.temperature), 2)
    humidity = round(float(bme280_data.humidity), 2)
    pressure = round(float(bme280_data.pressure), 2)
    # logging
    t_stamp_lg = f"Tiempo: {bme280_data.timestamp}"
    hum_lg = f"Humedad actual: {humidity} %"
    press_lg = f"Presion actual: {pressure} hPa"
    temp_lg = f"Temperatura: {temperature} °C"
    now = dt.datetime.today()
    head = now.strftime("%d/%m/%Y %H%M%S")
    print(head.center(50, "="))
    print(t_stamp_lg, hum_lg, press_lg, temp_lg, sep="\n")

    return {"humidity": humidity, "pressure": pressure,
            "temperature": temperature, }


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
    weather = influxdb_client.Point("weather").tag(
        "location", "office").field(
            "temperature", data["temperature"]).field(
            "humidity", data["humidity"]).field(
            "pressure", data["pressure"]
    )
    # cpu_temp = get_cpu_temp()

    write_api.write(bucket=bucket, org=org, record=weather)


if __name__ == "__main__":

    while True:
        try:
            data_point = read_sensor()
            write_data(data_point)
            sleep(5)
        except Exception as e:
            print(f"Exception has occured {e.args}")
