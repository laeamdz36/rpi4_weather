"""Module for read CPU temperature of raspberry"""
from gpiozero import LEDBarGraph, CPUTemperature



def get_cpu_temp():
    """Reading temperature from CPU"""

    cpu = CPUTemperature()
    print(f"Current temperature: {cpu.temperature}")

if __name__ == "__main__":
    get_cpu_temp()