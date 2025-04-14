#!/bin/bash

source "~/app_weather_1/.venv/bin/activate"

# Ejecuta el script Python (por ejemplo 'main.py')
python "~/app_weather_1//get_data.py"

# Opcional: desactiva el entorno virtual al finalizar
deactivate
