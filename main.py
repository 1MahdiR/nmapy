
###
# Main program, runs a user-interface and calls APIs
###

import os
from time import sleep
import platform
import socket
import subprocess

import ping

IS_WINDOWS = None # True if the os was windows
MAIN_MENU = '''
    _   __                ____
   / | / /___ ___  ____ _/ __ \__  __
  /  |/ / __ `__ \/ __ `/ /_/ / / / /
 / /|  / / / / / / /_/ / ____/ /_/ /
/_/ |_/_/ /_/ /_/\__,_/_/    \__, /
                            /____/

 1 > Ping a single host
 2 > Ping multiple hosts
 3 > Scan ports on a host
 4 > Traceroute a host
'''

main_menu = lambda: print(MAIN_MENU) # function for printing the main menu

# Set IS_WINDOWS variable
if platform.system().lower()=='windows':
    IS_WINDOWS = True
else:
    IS_WINDOWS = False

if IS_WINDOWS:
    clear = lambda: subprocess.call('cls')
else:
     clear = lambda: subprocess.call('clear')


### Program sections as functions ###
def ping_a_single_host():
    clear()
    print("\n--- Ping a single host ---\n")
    host = input("Enter a host address or ip: ").strip()

    try:
        host_ip = socket.gethostbyname(host)
    except:
        print("Unable to find {}. Ping failed.".format(host))
        input()
        return

    timeout = 0
    while True and timeout == 0:
        clear()
        print("\n--- Ping a single host ---\n")
        print("Host: {} ({})".format(host, host_ip))
        timeout = input("\ntimeout value (in seconds): ")
        if timeout.isdigit():
            timeout = float(timeout)
            if timeout > 0:
                break

    print("\nSending ICMP packets to {} ({})".format(host, host_ip))

    total_packets = 0
    packets_recieved = 0

    try:
        while True:
            tup = ping.ping(host_ip, timeout)
            total_packets += 1
            print(tup[1])
            if tup[0] == True:
                packets_recieved += 1
            sleep(1)
    except KeyboardInterrupt:
        print("\n{} packets transmitted, {} received, {:.2f}% packet loss".format(
                    total_packets, packets_recieved, ((total_packets- packets_recieved)/total_packets)*100))
        input()

def ping_multiple_hosts():
    ls_hosts = []

    while True:
        clear()
        print("\n--- Ping multiple hosts ---\n")
        if ls_hosts:
            print("Hosts: ")
            for i in ls_hosts:
                print("\t({})".format(i))
            print()
        new_host = input("Enter a host address or ip (Enter nothing to continue): ")
        if len(new_host.strip()) == 0:
            break
        ls_hosts.append(new_host)

    print()
    try:
        for host in ls_hosts:
            try:
                host_ip = socket.gethostbyname(host)
            except:
                print("FAILED: Unable to find {}. Ping failed.".format(host))
                continue
            tup = ping.ping(host_ip, 1)
            if tup[0] == True:
                print("RECIEVED: Recieved response from host {} ({})".format(host, host_ip))
            else:
                print("FAILED: Did not recieve a response from host {} ({})".format(host, host_ip))

        input()
    except KeyboardInterrupt:
        return

def scan_ports_on_a_host():
    print('scan_ports_on_a_host')
    sleep(1)

def traceroute_a_host():
    print('traceroute_a_host')
    sleep(1)

### Main menu controller ###
def main_menu_controller(s):
    if s == '1':
        ping_a_single_host()
    elif s == '2':
        ping_multiple_hosts()
    elif s == '3':
        scan_ports_on_a_host()
    else:
        traceroute_a_host()

while True:
    clear()
    main_menu()

    try:
        user_input = input('Command (1-4): ')

        if len(user_input) > 0 and user_input in "1234":
            main_menu_controller(user_input)

    except KeyboardInterrupt:
        print()
        break
