#done by Darilynn
from network import LoRa
import socket
import time
import ubinascii

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED0043CE8')
app_key = ubinascii.unhexlify('D60AF0A9C66B63E323DA99F14198EE91')
#using LoRaWAN application provided dev_eui
dev_eui = ubinascii.unhexlify('005E839F61F1B3DD')

# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)
# from network import LoRa
# import socket
import utime
# import binascii
import pycom
import ustruct
import machine
# from machine import ADC
#
# takes battery voltage readings
def adc_battery():

	adc = ADC(0)                                        # initialise adc hardware
	adc_c = adc.channel(attn=3, pin='P16')              # create an object to sample ADC on pin 16 with attenuation of 11db (config 3)
	adc_samples = []                                    # initialise the list
	for count in range(100):                            # take 100 samples and append them into the list
		adc_samples.append(int(adc_c()))

	adc_samples = sorted(adc_samples)                   # sort the list
	adc_median = adc_samples[int(len(adc_samples)/2)]   # take the center list row value (median average)
	# apply the function to scale to volts
	adc_median = adc_median * 2 / 4095 / 0.3275
	print(adc_samples)

	return adc_median

# disable LED heartbeat (so we can control the LED)
pycom.heartbeat(False)
# set LED to red
pycom.rgbled(0x7f0000)

# lora config
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)
# access info
app_eui = binascii.unhexlify('70B3D57ED0043CE8')
app_key = binascii.unhexlify('D60AF0A9C66B63E323DA99F14198EE91')

# attempt join - continues attempts background
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait for a connection
print('Waiting for LoRaWAN network connection...')
while not lora.has_joined():
	utime.sleep(1)
	# if no connection in a few seconds, then reboot
	if utime.time() > 15:
		print("possible timeout")
		machine.reset()
	pass

# we're online, set LED to green and notify via print
pycom.rgbled(0x007f00)
print('Network joined!')

# setup the socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.bind(1)

# sending some bytes
print('Sending 1,2,3')
s.send(bytes([1, 2, 3]))
utime.sleep(3)

#text is automatically converted to a string, data heavy (dont do it this way)
print('Sending "Hello World"')
s.send("Hello World!")
utime.sleep(3)

count = 0
# limit to 200 packets; just in case power is left on
while count <= 200:
	lipo_voltage = adc_battery()

	print("Battery voltage:  ", lipo_voltage)
	# encode the packet, so that it's in BYTES (TTN friendly)
	# could be extended like this struct.pack('f',lipo_voltage) + struct.pack('c',"example text")
	packet = ustruct.pack('f',lipo_voltage)

	# send the prepared packet via LoRa
	s.send(packet)

	# unpacking a payload
	print ("Unpacked value is:", ustruct.unpack('f',packet)[0])

	# check for a downlink payload, up to 64 bytes
	rx_pkt = s.recv(64)

	# check if a downlink was received
	if len(rx_pkt) > 0:
		print("Downlink data on port 200:", rx_pkt)
		pycom.rgbled(0xffa500)
		input("Downlink received, press Enter to continue")
		pycom.rgbled(0x007f00)

	count += 1
	utime.sleep(15)
