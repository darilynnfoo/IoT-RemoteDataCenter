#Done by Darilynn
from network import WLAN
wlan = WLAN()

wlan.init(mode=WLAN.AP, ssid='hello world')
wlan.init(ssid="Hi", auth=(WLAN.WPA2, "12345678"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface

#connecting to router
from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='FooFamily', auth=(WLAN.WPA2, 'Foofam0212'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully!")
print(wlan.ifconfig())

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
