import os
import time
import socket
from time import strftime
from datetime import datetime


default_mac = [ligne.rstrip('\n') for ligne in open("mac.txt", "r")]


def my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        global IP
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()


def scan():
    global mac_scan
    mac_scan = list()
    IP_S = IP.split(".")
    for a in range(1,256):
        IP_S[-1] = str(a)
        IP_P = ".".join(IP_S)
        ping_test = os.system(f' ping -c 2 {IP_P} > /dev/null ')
        if ping_test == 0:
            out = os.popen(f' arp -n {IP_P} | grep -E "^[0-9]{{2,3}}" ').read().splitlines()
            for i, line in enumerate(out, start=1):
                mac = line.split()[2]
                mac_scan.append(mac)
        else:
            pass
    mac_scan.remove('--')


def compare():
    scan()
    for j in range(0,len(mac_scan)):
        if mac_scan[j] in default_mac:
            print("Pass")
        else:
            print("Intrusion :",mac_scan[j])


def listen():
    old_mac = len(mac_scan)
    while True:
        scan()
        nb_mac = len(mac_scan)
        #Comparaison
        if nb_mac > old_mac:
            if mac_scan[old_mac] in default_mac:
                print(datetime.now().strftime("%d %B %Y  %H:%M:%S"),": Connected:",mac_scan[old_mac])
            else:
                print(datetime.now().strftime("%d %B %Y  %H:%M:%S"),": Intrusion:",mac_scan[old_mac])
        elif nb_mac < old_mac:
            print(datetime.now().strftime("%d %B %Y  %H:%M:%S"),": Deconnected")
        else:
            print(datetime.now().strftime("%d %B %Y  %H:%M:%S"),": No change")

        old_mac = nb_mac


if __name__=="__main__":
    my_ip()
    compare()
    listen()