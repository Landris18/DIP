import os
import time

default_mac = [ligne.rstrip('\n') for ligne in open("mac.txt", "r")]

def scan():
    global mac_scan
    mac_scan = list()
    out = os.popen(' /sbin/arp-scan --localnet | grep -E "^[0-9]{2,3}" ').read().splitlines()
    for i, line in enumerate(out, start=1):
        mac = line.split()[1]
        mac_scan.append(mac)
  


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
            if mac_scan[old_mac] in  default_mac:
                pass
            else:
                print("Intrusion:",mac_scan[old_mac])
        elif nb_mac < old_mac:
            print("Deconnected")
        else:
            print("No change")

        time.sleep(5)
        old_mac = nb_mac




if __name__=="__main__":
    compare()
    listen()