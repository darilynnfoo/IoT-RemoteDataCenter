#Done by Darilynn
import pycom
import time
import machine
from network import WLAN
wlan = WLAN()

wlan.init(mode=WLAN.AP, ssid='hello world')
#use the line below to apply a password
#wlan.init(ssid="hi", auth=(WLAN.WPA2, "eightletters"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface

#connecting to router
#from network import WLAN

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='Foofamily', auth=(WLAN.WPA2, 'Foofam0212'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

#scanning wifi networks
#from network import WLAN
#import machine
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'Foofamily':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'Foofam0212'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

#done by Jaya

#import machine
#from network import WLAN
wlan = WLAN() # get current object, without changing the mode
if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.178.107', '255.255.255.0', '192.168.1.10', '8.8.8.8')) # (ip, subnet_mask, gateway, DNS_server)

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('mywifi', auth=(WLAN.WPA2, 'mywifikey'), timeout=5000)
    print("connecting",end='')
    while not wlan.isconnected():
        time.sleep(1)
        print(".",end='')
    print("connected")

#done by Darilynn
# connecting using external antenna
# from network import WLAN
# wlan = WLAN()
wlan.antenna(WLAN.EXT_ANT)
