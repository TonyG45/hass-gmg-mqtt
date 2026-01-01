import time
import paho.mqtt.client as mqtt
from gmg import grills

BASE_TOPIC = "gmg/grill"
POLL_INTERVAL = 5

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT:", rc)
    client.subscribe(f"{BASE_TOPIC}/set/#")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("MQTT command:", msg.topic, payload)

    if msg.topic.endswith("/setpoint"):
        grill.set_temp(int(payload))
    elif msg.topic.endswith("/power"):
        if payload == "ON":
            grill.power_on()
        elif payload == "OFF":
            grill.power_off()

# Connect to MQTT (use Mosquitto add-on hostname)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("core-mosquitto", 1883, 60)
client.loop_start()

print("Discovering GMG grill...")
grill = grills(2)[0]
print("Found grill:", grill._serial_number)

while True:
    state = grill.status()

    client.publish(f"{BASE_TOPIC}/temperature", state["temp"])
    client.publish(f"{BASE_TOPIC}/setpoint", state["grill_set_temp"])
    client.publish(f"{BASE_TOPIC}/power", "ON" if state["on"] else "OFF")
    client.publish(f"{BASE_TOPIC}/probe/1", state["probe1_temp"])
    client.publish(f"{BASE_TOPIC}/probe/2", state["probe2_temp"])

    time.sleep(POLL_INTERVAL)
