"""Module for continous get data from Sensor BME"""

import datetime as dt
import os


def dev_logger_time():
    """For development testing call this function to print time"""

    print(dt.datetime.now())

def get_env_mode():
    """Get the env variable "RUNMODE", to check if deploy is in dev or production"""

    r_mode = os.getenv("RUNMODE")
    return r_mode

def read_sensor_data():
    """Run configuration for sensor"""
    import bme280
    import smbus2

    port = 1
    address = 0x76  # Adafruit BME280 address. Other BME280s may be different
    bus = smbus2.SMBus(port)
    bme280.load_calibration_params(bus, address)

    bme280_data = bme280.sample(bus, address)

    bme280_data = bme280.sample(bus, address)
    time_stamp = f"Tiempo: {bme280_data.timestamp}"
    humidity = f"Humedad actual: {bme280_data.humidity} %"
    pressure = f"Presion actual: {bme280_data.pressure} hPa"
    ambient_temperature = f"Temperatura: {bme280_data.temperature} °C"
    data = [humidity, pressure, ambient_temperature]
    return  data

def main():
    """Execute reading"""
    data = read_sensor_data()

if __name__ == "__main__":
    # read env variable
    run_mode = get_env_mode()
    if run_mode == "dev":
        dev_logger_time()
    else:
        main()