ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir paho-mqtt gmg

COPY gmg_mqtt_bridge.py .

CMD ["python3", "gmg_mqtt_bridge.py"]
