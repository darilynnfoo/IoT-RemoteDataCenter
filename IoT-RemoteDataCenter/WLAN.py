#Done by Darilynn
import pycom
import time
import machine
from network import WLAN
wlan = WLAN()

wlan.init(mode=WLAN.AP, ssid='hello world')
wlan.init(ssid="Hi", auth=(WLAN.WPA2, "12345678"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface

#connecting to router
#from network import WLAN

wlan = WLAN(mode=WLAN.STA)

<<<<<<< HEAD:IoT-RemoteDataCenter/WLAN.py
<<<<<<< HEAD
wlan.connect(ssid='FooFamily', auth=(WLAN.WPA2, 'Foofam0212'))
=======
wlan.connect(ssid='suriya', auth=(WLAN.WPA2, 'jaya123suriya456'))
>>>>>>> 4d6e722e5430c527f343113f70c01f39a86d697e
=======
wlan.connect(ssid='Blk 805', auth=(WLAN.WPA2, 'Theju123'))
>>>>>>> 7a8ae6938afd6074dc06fc4f781d8f4319e4691c:RGB-Blink/WLAN.py
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully!")
print(wlan.ifconfig())

<<<<<<< HEAD
# #scanning wifi network only for wireless router
# from network import WLAN
# import machine
# wlan = WLAN(mode=WLAN.STA)
#
# nets = wlan.scan()
# for net in nets:
#     if net.ssid == 'FooFamily':
#         print('Network found!')
#         wlan.connect(net.ssid, auth=(net.sec, 'Foofam0212'), timeout=5000)
#         while not wlan.isconnected():
#             machine.idle() # save power while waiting
#         print('WLAN connection succeeded!')
#         break

# connecting to WPA-2
# from network import WLAN
#
# wlan = WLAN(mode=WLAN.STA)
# wlan.connect(ssid='mywifi', auth=(WLAN.WPA2_ENT,), identity='myidentity', ca_certs='/flash/cert/ca.pem', keyfile='/flash/cert/client.key', certfile='/flash/cert/client.crt')
=======
#scanning wifi networks
#from network import WLAN
#import machine
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'Blk 805':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'Theju123'), timeout=5000)
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

>>>>>>> 4d6e722e5430c527f343113f70c01f39a86d697e
