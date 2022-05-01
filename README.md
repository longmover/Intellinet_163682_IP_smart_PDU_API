# Intellinet IP smart PDU API [163682]
A python API wrapper for Intellinet IP smart PDU [163682] that allows you to do anything that the web interface provides.
You can:
* read all sensors (humidity, temperature)
* read voltages
* get states of outlets
* turn outlets on/off/toffle
* read and set warning levels
* ...

You can get one here: https://www.amazon.com/dp/B075TXJFWN (this is not a referral link)

Sample images from amazon:

![Intellinet smart PDU](https://images-na.ssl-images-amazon.com/images/I/61GjeHxLTrL._SL1500_.jpg)
![Intellinet smart PDU 2](https://images-na.ssl-images-amazon.com/images/I/61uYPCVnsmL._SL1500_.jpg)

Now also includes a python script which can be run as a service to control the PDU via MQTT, also supports Home Assistant discovery.  All based on https://github.com/01programs excellent original API wrapper.

Arguments:
- host : hostname or ip of the PDU
- --mqtt
-   host : hostname or IP of your MQTT broker
-   port : port to use for MQTT
-   user : MQTT username
-   pass : MQTT password

Example: pdu_control.py 10.0.0.10 --mqtt 10.0.0.15 1883 mqtt_user mqtt_pwd123

Providing all arguments are accurate the script will establish a link to the MQTT broker and publish the discovery messages for HA integration.  Status updates will publish every 5 seconds.  Currently the status reported by the device is not included in the sensors, I plan to add this soon.

I am new to Python but learning, happy to have any comments/suggestions/criticisms

MQTT baseline code based on https://github.com/tinaught/appkettleapi
