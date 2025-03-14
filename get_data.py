"""Module for reading data for raspberry PI SPI interface sensor"""

import bme280
import smbus2
from gpiozero import LED
import time
# from time import sleep


def en_relay():
    """Testing reading GPIO"""

    rel1 = LED(17)

    rel1.on()
    time.sleep(3)
    rel1.off()
    time.sleep(1)
    rel1.on()
    time.sleep(1)


def blink_relay():
    """testing blinking relay"""

    relay = LED(17)
    relay.blink(on_time=1, off_time=1, n=10)


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

    print(time_stamp, humidity, pressure, ambient_temperature, sep="\n")

    return {"humidity": humidity, "pressure": pressure,
            "ambient_temperature": ambient_temperature, }


if __name__ == "__main__":
    read_sensor()
    # en_relay()
    blink_relay()
