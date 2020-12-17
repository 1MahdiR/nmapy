
###
# Main program, runs a user-interface and calls APIs
###

import os
from time import sleep
import platform
import socket
import subprocess

import ping
import port_scanner
import traceroute

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

    try:
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
        while True:
            clear()
            print("\n--- Ping a single host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            timeout = input("\ntimeout value (in seconds): ")
            try:
                timeout = float(timeout)
                if timeout > 0:
                    break
            except:
                continue

        print("\nSending ICMP packets to {} ({})".format(host, host_ip))

    except KeyboardInterrupt:
        return

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
        try:
            input()
        except KeyboardInterrupt:
            return

def ping_multiple_hosts():

    try:
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

        for host in ls_hosts:
            try:
                host_ip = socket.gethostbyname(host)
            except:
                print("FAILED: Unable to find {}. Ping failed.".format(host))
                continue
            tup = ping.ping(host_ip, 1)
            if tup[0] == True:
                print("RECIEVED: Recieved response from {} ({})".format(host, host_ip))
            else:
                print("FAILED: Did not recieve a response from host {} ({})".format(host, host_ip))

        input()
    except KeyboardInterrupt:
        return

def scan_ports_on_a_host():

    try:
        clear()
        print("\n--- Scan ports on a host ---\n")
        host = input("Enter a host address or ip: ").strip()

        try:
            host_ip = socket.gethostbyname(host)
        except:
            print("Unable to find {}. Port scan failed.".format(host))
            input()
            return

        while True:
            clear()
            print("\n--- Scan ports on a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            port_range = input("\nEnter the port number range (1-65534): ").split(":")
            try:
                if len(port_range) == 1 or port_range[0] == port_range[1]:
                    port_range = [int(port_range[0]), int(port_range[0])+1]
                else:
                    port_range = [int(port_range[0]), int(port_range[1])+1]
            except:
                continue

            if port_range[0] <= port_range[1] and port_range[0] > 0 and port_range[1] > 0:
                break

        while True:
            clear()
            print("\n--- Ping a single host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("\nPort range: ({}-{})".format(port_range[0], port_range[1]))
            timeout = input("\ntimeout value (in seconds): ")
            try:
                timeout = float(timeout)
                if timeout > 0:
                    break
            except:
                continue

        print("\nChecking ports ({}-{}) of {} ({})".format(port_range[0], port_range[1]-1,
                                                            host, host_ip))
        open_ports = port_scanner.port_scan(host_ip, (port_range[0], port_range[1]), timeout=timeout)

        print("\nOpen ports in ({}-{}):".format(port_range[0], port_range[1]))
        if open_ports:
            for i in open_ports:
                print("\t{}".format(i))
        else:
            print("\tNo open ports")
        input()

    except KeyboardInterrupt:
        return

def traceroute_a_host():
    try:
        clear()
        print("\n--- Traceroute a host ---\n")
        host = input("Enter a host address or ip: ").strip()

        try:
            host_ip = socket.gethostbyname(host)
        except:
            print("Unable to find {}. Traceroute failed.".format(host))
            input()
            return

        hops = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            hops = input("\nnumber of hops: ")
            try:
                hops = int(hops)
                if hops > 0:
                    break
            except:
                continue

        size = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("Hops: {}".format(hops))
            size = input("\npacket size (in bytes): ")
            try:
                size = int(size)
                if size > 0:
                    break
            except:
                continue

        timeout = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("Hops: {}".format(hops))
            print("Size: {} bytes".format(size))
            timeout = input("\ntimeout value (in seconds): ")
            try:
                timeout = float(timeout)
                if timeout > 0:
                    break
            except:
                continue

        print("\nTraceroute to {} ({})\n maximum hops: {}\n {} byte packets\n".format(host, host_ip, hops, size))
        traceroute.traceroute(host_ip, hops=hops, size=size, timeout=timeout)
        input()

    except KeyboardInterrupt:
        return

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
        user_input = input('Command (1-4): ').strip()

        if len(user_input) == 1 and user_input in "1234":
            main_menu_controller(user_input)

    except KeyboardInterrupt:
        print()
        break
