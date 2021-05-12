#Done by Darilynn
from network import WLAN
wlan = WLAN()

wlan.init(mode=WLAN.AP, ssid='hello world')
#use the line below to apply a password
#wlan.init(ssid="hi", auth=(WLAN.WPA2, "eightletters"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface

#connecting to router
from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='ssid', auth=(WLAN.WPA2, 'password'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

#scanning wifi networks
from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'mywifi':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'mywifikey'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
