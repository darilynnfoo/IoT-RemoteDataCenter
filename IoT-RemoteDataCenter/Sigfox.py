#Done by Darilynn

#Retrieving SigFox ID and PAC
from network import Sigfox
import binascii
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
# print Sigfox Device ID
print(binascii.hexlify(sigfox.id()))
# print Sigfox PAC number
print(binascii.hexlify(sigfox.pac()))


#Downlink message
from network import Sigfox
import socket
# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# make socket blocking
s.setblocking(True)
# configure it as DOWNLINK specified by 'True'
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
# send some bytes and request DOWNLINK
s.send(bytes([1, 2, 3]))
# await DOWNLINK message
r = s.recv(32)
print(ubinascii.hexlify(r))


#communicating device to device
#DEVICE 1
from network import Sigfox
import socket
sigfox = Sigfox(mode=Sigfox.FSK, frequency=868000000)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
while True:
  s.send('Device-1')
  time.sleep(1)
  print(s.recv(64))
  
#DEVICE 2
from network import Sigfox
import socket
sigfox = Sigfox(mode=Sigfox.FSK, frequency=868000000)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
while True:
  s.send('Device-2')
  time.sleep(1)
  print(s.recv(64))
