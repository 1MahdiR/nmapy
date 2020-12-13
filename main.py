
###
# Main program, runs a user-interface and calls APIs
###

import os
from time import sleep
import platform
import subprocess

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
    print('ping_a_single_host')
    sleep(1)

def ping_multiple_hosts():
    print('ping_multiple_hosts')
    sleep(1)

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
