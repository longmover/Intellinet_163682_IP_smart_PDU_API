import ip_pdu
import json
import argparse
import time
import paho.mqtt.client as mqtt     # pip install paho.mqtt

MQTT_BASE = "ipPDU/"
MQTT_COMMAND_TOPIC = MQTT_BASE + "command"
MQTT_STATUS_TOPIC = MQTT_BASE + "status"
MQTT_HA_AUTODISCOVERY_TOPIC = "homeassistant/switch/" + "ipPDU"

def mainLoop(host, mqtt_broker):
    if not mqtt_broker is None:
        pdu = ip_pdu.IPU(host)
        mqttc = mqtt.Client()
        if not mqtt_broker[2] is None:
            mqttc.username_pw_set(mqtt_broker[2], password=mqtt_broker[3])
            mqttc.on_connect = cb_mqtt_on_connect
            mqttc.on_message = cb_mqtt_on_message
            mqttc.user_data_set(pdu)  # passes to each callback $pdu as $userdata
            mqttc.will_set(MQTT_STATUS_TOPIC + "/status", "offline", retain=True)
            mqttc.connect(mqtt_broker[0], int(mqtt_broker[1]))
            mqttc.loop_start()
            #publish HA autodiscovery details
            for i in range(0,8)
                mqttc.publish(MQTT_HA_AUTODISCOVERY_TOPIC + 'switch_' + str(i) + '/config','{"availability": [{"topic": "ipPDU/status/status"}],"command_topic": "ipPDU/command/outlets/' + str(i) + '","device": {"identifiers": ["ipPDU_outlet_' + str(i) + '"], "manufacturer": "Intellinet", "model": "IP smart PDU", "name": "ipPDU_outlet_' + str(i) + '"}, "name": "ipPDU_outlet_' + str(i) + '", "payload_off": "OFF", "payload_on": "ON", "state_topic": "ipPDU/status/outlets/' + str(i) + '", "unique_id": "ipPDU_outlet_' + str(i) + '_pdu_control"}', retain=True)
            while True:
                if not mqtt_broker is None:
                    mqttc.publish(MQTT_STATUS_TOPIC + "/STATE", json.dumps(pdu.status(), indent = 2))
                    mqttc.publish(MQTT_STATUS_TOPIC + "/status", "online", retain=True)
                time.sleep(5)


def cb_mqtt_on_connect(client, flags, rec_code):
    """ The callback for when the client receives a CONNACK response from the server. """
    print("Connected to MQTT broker with result code " + str(rec_code))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_COMMAND_TOPIC + "/#")  # subscribe to all topics

def cb_mqtt_on_message(mqttc, pdu, msg):
    """ The callback for when a PUBLISH message is received from the server. """
#add test that last char is digit within limits with preceding "/"
    if msg.topic == MQTT_COMMAND_TOPIC + "/outlets/" + msg.topic[-1:]:
        outlet = msg.topic[-1:]
        if msg.payload == b'ON':
            pdu.enable_outlets(outlet)
        elif msg.payload == b'OFF':
            pdu.disable_outlets(outlet)
        else:
            print("MQTT MSG: msg not recognised:", msg)
        mqttc.publish(MQTT_STATUS_TOPIC + "/STATE", json.dumps(pdu.status(), indent = 2))
        states = pdu.status() #get full pdu status
        for i in range(len(states["outlet_states"])): #for each outlet publish a status update
            mqttc.publish(MQTT_STATUS_TOPIC + "/outlets/" + str(i),states["outlet_states"][i])

def getStatus(host):
    pdu = ip_pdu.IPU(host)
    #json_object = json.dumps(pdu.status(), indent = 2)
    return pdu

def argparser():
    """Parses input arguments, see -h"""
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", help="PDU host or IP")

    parser.add_argument(
        "--mqtt",
        help="MQTT broker host, port, username & password (e.g. --mqtt 192.168.0.1 1883 mqtt_user p@55w0Rd)",
        nargs=4,
        metavar=("host", "port", "username", "password"),
    )

    args = parser.parse_args()
    mainLoop(args.host, args.mqtt)

if __name__ == "__main__":
    argparser()
