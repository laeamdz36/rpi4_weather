FROM ubuntu/python:3.12-24.04
LABEL authors="luipen366"
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV RUNMODE=dev
CMD ["python3", "cont_get_data.py"]