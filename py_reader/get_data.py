"""Module for reading data for raspberry PI SPI interface sensor"""

import os
from time import sleep
import datetime as dt
import bme280
import smbus2
import paho.mqtt.client as mqtt
from gpiozero import CPUTemperature
from gpiozero.pins.native import NativeFactory
from gpiozero import Device
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


def get_cpu_temp():
    """Reading temperature from CPU"""
    cpu = None
    try:
        cpu = CPUTemperature()
        print(f"Current temperature: {cpu.temperature}")
        cpu = round(float(cpu.temperature), 2)
    except Exception as e:
        print(f"Error: {e.args}")
    return cpu


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
    weather = influxdb_client.Point("weather").tag(
        "location", "office").field(
            "temperature", data["temperature"]).field(
            "humidity", data["humidity"]).field(
            "pressure", data["pressure"]
    )
    # cpu_temp = get_cpu_temp()

    write_api.write(bucket=bucket, org=org, record=weather)


def load_topics(selector=None):
    """Return topic selected"""

    # build topics for each sensor
    _topics = None
    if selector is None:
        _topic = "rp1/weather"
        _names = ["temperature", "humidity", "pressure"]
        _topics = {_name: {"topic": _top} for _name,
                   _top in zip(_names, [f"{_topic}/{x}" for x in _names])}
    return _topics


def create_mqtt_client():
    """Create MQTT client to connection"""

    BROKER = "192.168.68.109"
    PORT = 1883
    username = "mqtt_usr"
    password = "luismdz366"
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(BROKER, PORT, 60)
    return client


def pub_mqtt(client, data):
    """Publish MQTT"""

    _topics = load_topics()
    try:
        cputemp = get_cpu_temp()
        if cputemp:
            client.publish("rp1/system/cpu_temp", cputemp)
        print(f"PUB: rp1/system/cpu_temp - {cputemp}")
        for sensor, value in data.items():
            client.publish(_topics.get(sensor)["topic"], value)
            print(
                f"Pub topic: {_topics.get(sensor)["topic"]}, val: {value}")
    except Exception as e:
        print(f"ERROR: {e.args}")
    finally:
        client.disconnect()


if __name__ == "__main__":

    Device.pin_factory = NativeFactory()
    _client = create_mqtt_client()
    while True:
        try:
            # read sensor BME280
            data_point = read_sensor()
            # write data into influxdb
            write_data(data_point)
            # publish data to MQTT
            pub_mqtt(_client, data_point)
            sleep(5)
        except Exception as e:
            print(f"Exception has occured {e.args}")
