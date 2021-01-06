
###
# A simple network tool written in python
#
# by MR
# Script is available on github: https://github.com/1MahdiR/nmapy
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
 0 > Exit
'''

main_menu = lambda: print(MAIN_MENU) # function for printing the main menu

# Set IS_WINDOWS variable
if platform.system().lower()=='windows':
    IS_WINDOWS = True
else:
    IS_WINDOWS = False

# function for clearing the console
if IS_WINDOWS:
    clear = lambda: os.system('cls')
else:
     clear = lambda: subprocess.call('clear')


### Program sections as functions ###
def ping_a_single_host():

    try:
        clear()
        print("\n--- Ping a single host ---\n")
        host = input("Enter a host address or ip: ").strip()

        ### tries to resolve host address to ip
        ### if resolve fails function will return
        try:
            host_ip = socket.gethostbyname(host)
        except:
            print("Unable to find {}. Ping failed.".format(host))
            input()
            return


        ### get how many packets will be sent from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        ### the default value is 0 which will ping the host continuously
        while True:
            clear()
            print("\n--- Ping a single host ---\n")
            print("Host: {} ({})".format(host, host_ip))

            ### default value: 0
            count = input("\nNumber of packets [0]: ").strip()
            if not count.isdigit() and count != '':
                continue
            if count == "":
                count = 0
            try:
                count = int(count)
                if count >= 0:
                    break
            except:
                continue

        cont_ping = True if count == 0 else False

        ### get the timeout value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        timeout = 0
        while True:
            clear()
            print("\n--- Ping a single host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            if cont_ping:
                print("Number of packets: continuously")
            else:
                print("Number of packets: {}".format(count))

            ### default timeout value: 1
            timeout = input("\ntimeout value (in seconds) [1]: ").strip()
            if timeout == "":
                timeout = 1
            try:
                timeout = float(timeout)
                if timeout > 0:
                    break
            except:
                continue

        print("\nSending ICMP packets to {} ({})".format(host, host_ip))

    ### will return to main menu with a keyboard interrupt (Ctrl+C)
    except (KeyboardInterrupt, EOFError):
        return

    total_packets = 0
    packets_recieved = 0

    try:
        while count > 0 or cont_ping:
            total_packets += 1 ### total packets increment
            tup = ping.ping(host_ip, timeout)
            print(tup[1])
            if tup[0] == True:  ### if received an ICMP reply
                packets_recieved += 1
            count -= 1
            sleep(1)

    ### will stop the ping with a keyboard interrupt (Ctrl+C)
    except KeyboardInterrupt:
            pass

    finally:

        ### showing results of ping
        print("\n{} packets transmitted, {} received, {:.2f}% packet loss".format(
                    total_packets, packets_recieved, ((total_packets - packets_recieved)/total_packets)*100))
        try:
            input()

        ### will return to main menu with a keyboard interrupt (Ctrl+C)
        except (KeyboardInterrupt, EOFError):
            return

def ping_multiple_hosts():

    try:
        ls_hosts = []

        ### get the host addresses from user
        ### this loop will repeat until user enters blank string
        while True:
            clear()
            print("\n--- Ping multiple hosts ---\n")
            if ls_hosts:
                print("Hosts: ")
                for i in ls_hosts:
                    print("\t({})".format(i))
                print()
            new_host = input("Enter a host address or ip (Enter nothing to continue): ")
            if len(new_host.strip()) == 0 and len(ls_hosts) != 0:
                break
            elif len(new_host.strip()) != 0:
                ls_hosts.append(new_host)

        print()

        for host in ls_hosts:
            ### tries to resolve host address to ip
            ### if resolve fails a FAILED message will be shown
            try:
                host_ip = socket.gethostbyname(host)
            except:
                print("FAILED: Unable to find {}. Ping failed.".format(host)) ### if resolve fails
                continue
            tup = ping.ping(host_ip, 2) ### send an ICMP packet to host
            if tup[0] == True: ### if recieved an ICMP reply
                print("RECIEVED: Recieved response from {} ({})".format(host, host_ip))
            else:
                print("FAILED: Did not recieve a response from host {} ({})".format(host, host_ip))

        input()

    ### will return to main menu with a keyboard interrupt (Ctrl+C)
    except (KeyboardInterrupt, EOFError):
        return

def scan_ports_on_a_host():

    try:
        clear()
        print("\n--- Scan ports on a host ---\n")
        host = input("Enter a host address or ip: ").strip()

        ### tries to resolve host address to ip
        ### if resolve fails function will return
        try:
            host_ip = socket.gethostbyname(host)
        except:
            print("Unable to find {}. Port scan failed.".format(host))
            input()
            return

        ### get the port number range value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        while True:
            clear()
            print("\n--- Scan ports on a host ---\n")
            print("Host: {} ({})".format(host, host_ip))

            ### default port number range value: 1:65535
            port_range = input("\nEnter the port number range (1-65535) [1:65535]: ").strip()
            if port_range == "":
                port_range = "1:65535"
            port_range = port_range.split(':')
            if not port_range[0].isdigit() or not port_range[1].isdigit():
                continue
            try:

                if len(port_range) == 1 or port_range[0] == port_range[1]: ### if one port was specified
                    port_range = [int(port_range[0]), int(port_range[0])+1]
                else:
                    port_range = [int(port_range[0]), int(port_range[1])+1]
            except:
                continue

            ### validating user input values
            if port_range[0] <= port_range[1] and port_range[0] > 0 and port_range[1]-1 > 0:
                if port_range[0] < 65536 and port_range[1]-1 < 65536:
                    break

        ### get the timeout value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        while True:
            clear()
            print("\n--- Scan ports on a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("\nPort range: ({}-{})".format(port_range[0], port_range[1]))

            ### default timeout value: 1
            timeout = input("\ntimeout value (in seconds) [1]: ").strip()
            if timeout == "":
                timeout = 1
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
        if open_ports: ### if open_ports was not empty
            for i in open_ports:
                print("\t{}".format(i))
        else:
            print("\tNo open ports")
        input()

    ### will return to main menu with a keyboard interrupt (Ctrl+C)
    except (KeyboardInterrupt, EOFError):
        return

def traceroute_a_host():
    try:
        clear()
        print("\n--- Traceroute a host ---\n")
        host = input("Enter a host address or ip: ").strip()

        ### tries to resolve host address to ip
        ### if resolve fails function will return
        try:
            host_ip = socket.gethostbyname(host)
        except:
            print("Unable to find {}. Traceroute failed.".format(host))
            input()
            return

        ### get the hops value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        hops = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))

            ### default hops value: 30
            hops = input("\nnumber of hops [30]: ").strip()
            if hops == "":
                hops = 30
            try:
                hops = int(hops)
                if hops > 0:
                    break
            except:
                continue

        ### get the packet size value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        size = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("Hops: {}".format(hops))

            ### default size value: 60
            size = input("\npacket size (in bytes) [60]: ").strip()
            if size == "":
                size = 60
            try:
                size = int(size)
                if size > 0:
                    break
            except:
                continue

        ### get the timeout value from user
        ### this loop will repeat until user enters a valid value
        ### if user enters a blank string the default value will be set
        timeout = 0
        while True:
            clear()
            print("\n--- Traceroute a host ---\n")
            print("Host: {} ({})".format(host, host_ip))
            print("Hops: {}".format(hops))
            print("Size: {} bytes".format(size))

            ### default timeout value
            timeout = input("\ntimeout value (in seconds) [1]: ").strip()
            if timeout == "":
                timeout = 1
            try:
                timeout = float(timeout)
                if timeout > 0:
                    break
            except:
                continue

        print("\nTraceroute to {} ({})\n maximum hops: {}\n {} byte packets\n".format(host, host_ip, hops, size))
        traceroute.traceroute(host_ip, hops=hops, size=size, timeout=timeout)
        input()

    ### will return to main menu with a keyboard interrupt (Ctrl+C)
    except (KeyboardInterrupt, EOFError):
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

### Main menu ###
while True:
    clear()
    main_menu()

    try:
        user_input = input('Command (1-4): ').strip()

        ### validating main menu command
        if len(user_input) == 1 and user_input in "01234":
            if user_input == "0":
                break
            main_menu_controller(user_input)

    except (KeyboardInterrupt, EOFError):
        print()
        break
