"""Module for reading data for raspberry PI SPI interface sensor"""

import bme280
import smbus2
# from time import sleep

# adding comment

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