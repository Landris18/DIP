from scapy.all import *
import netifaces


def get_gateway_address():
    gateways = netifaces.gateways()
    global gateway_address
    gateway_address = gateways["default"][netifaces.AF_INET][0]
    print(gateway_address)


def connected(gateway_address, ip_range):
     arp_request = ARP(pdst=ip_range)
     broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
     arp_request_broadcast = broadcast/arp_request
     response = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
     clients = []
     for client in response:
          client_info = {"ip" : client[1].psrc, "mac" : client[1].src}
          clients.append(client_info)
     print(clients)


def call_connected():
     class_a = [i for i in range(127)]
     class_b = [i for i in range(127,192)]
     class_c = [i for i in range(192,224)]
     g_s = gateway_address.split('.')
     g_s[-1] = '0'
     range_ip = ".".join(g_s)
     if int(g_s[0]) in class_a:
          connected(gateway_address, f'{range_ip}/8')
     elif int(g_s[0]) in class_b:
          connected(gateway_address, f'{range_ip}/16')
     elif int(g_s[0]) in class_c:
          connected(gateway_address, f'{range_ip}/24')
     else:
          print("Adresse IP non prise en charge")


if __name__ == "__main__":
    get_gateway_address()
    call_connected()