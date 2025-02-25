"""OPC server for publish data from sensor BME280"""

import os
import asyncio
import logging
import get_data
import get_cpu_temo
from asyncua import Server


async def main():

    prod_port = os.getenv("PROD_PORT")
    if prod_port is None:
        prod_port = "3700"

    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint(f"opc.tcp://0.0.0.0:{int(prod_port)}/pyopc/weather/")

    # set up our own namespace, not really necessary but should as spec
    uri = "opc_weather_rasp1"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    station1 = await server.nodes.objects.add_object(idx, "Station1")
    temperature = await station1.add_variable(idx, "temperature", 30.0)
    pressure = await station1.add_variable(idx, "pressure", 1000.0)
    humidity = await station1.add_variable(idx, "humidity", 60.0)
    cpu_temp = await station1.add_variable(idx, "humidity", 60.0)
    # Definition of variables to be writables
    await temperature.set_writable()
    await pressure.set_writable()
    await humidity.set_writable()
    await cpu_temp.set_writable()

    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            # get variables
            values = get_data.read_sensor()
            cpu_temp = get_cpu_temo.get_cpu_temp()

            upd_temperature = values.get("ambient_temperature")
            upd_pressure = values.get("pressure")
            upd_humidity = values.get("humidity")

            # write in variables to update its values
            await temperature.write_value(upd_temperature)
            await humidity.write_value(upd_humidity)
            await pressure.write_value(upd_pressure)
            await cpu_temp.write_value(cpu_temp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)