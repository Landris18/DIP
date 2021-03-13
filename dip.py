import os
import socket
import time
from time import strftime
from datetime import datetime
from threading import Thread


default_mac = [ligne.rstrip('\n') for ligne in open("mac.txt", "r")]


#Getting your local IP
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

#Scanning network to get connected devices
def scan():
    def ping(ip):
        ping_test = os.system(f' ping -c 2 {ip} > /dev/null ')
        if ping_test == 0:
            out = os.popen(f' arp -n {ip} | grep -E "^[0-9]{{2,3}}" ').read().splitlines()
            global mac_scan
            for i, line in enumerate(out, start=1):
                mac = line.split()[2]
                mac_scan.append(mac)
        else:
            pass
        try: mac_scan.remove('--')
        except: pass

    global mac_scan
    mac_scan = list()
    IP_S = IP.split(".")
    prs = []
    for a in range(1,255):
        IP_S[-1] = str(a)
        IP_P = ".".join(IP_S)
        p = Thread(target=ping, args=[IP_P])
        p.start()
        prs.append(p)
    for pr in prs:
        pr.join()


    
def compare():
    scan()
    print("------COMPARAISON DES ADRESSES MACS------")
    for j in range(0,len(mac_scan)):
        if mac_scan[j] in default_mac:
            print("Pass")
        else:
            print("Intrusion :",mac_scan[j])
    print('''
    ---------------------------------------


    ''')
    
    


#Listenning the network in realtime            
def listen():
    print("-----------ECOUTE DU RESEAU------------")
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
