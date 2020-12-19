
###
# Implements traceroute with ping utility
###

import platform
import subprocess
import socket
import re

# This function will get ping data by processing its output
# ping argument must be an ip address
def parse_ping_output(output):

    ip_pattern = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"

    is_windows = False
    if platform.system().lower()=='windows':
        is_windows = True

    ls = re.findall(ip_pattern, output)
    if not is_windows:
        if len(ls) < 3:
            raise Exception("Bad output to process")

        ls = ls[1:-1]

        # if no ICMP reply recieved return a '*' and false
        if len(ls) < 2:
            return (False, '*')

        # if ttl of packet exceeded return false
        if re.search('Time to live exceeded', output):
            return (False, ls[1])

        # if packet reached its destination return true
        if ls[0] == ls[1]:
            return (True, ls[1])

    else:
        if len(ls) < 2:
            raise Exception("Bad output to process")

        ls = ls[:-1]

        # if no ICMP reply recieved return a '*' and false
        if len(ls) < 2:
            return (False, '*')

        # if ttl of packet exceeded return false
        if re.search('TTL expired in transit', output):
            return (False, ls[1])

            # if packet reached its destination return true
        if ls[0] == ls[1]:
            return (True, ls[1])

    raise Exception("Unexpected error")

def traceroute(host_ip, hops=30, size=60, timeout=5):

    def f(host, ttl):

        count_param = '-n' if platform.system().lower()=='windows' else '-c' # ping count parameter
        ttl_param = '-i' if platform.system().lower()=='windows' else '-t' # ping time to live paramter
        size_param = '-l' if platform.system().lower()=='windows' else '-s' # ping packet size parameter
        timeout_param = '-w' if platform.system().lower()=='windows' else '-W' # ping timeout parameter

        command = ['ping', count_param, '1', ttl_param, str(ttl), size_param, str(size), timeout_param, str(timeout), host]

        # returns ping output as bytes
        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # returns true, if a packet reaches its destination within specified hops
    for ttl in range(1, hops+1):
        output = f(host_ip, ttl)
        tup = parse_ping_output(output.stdout.read().decode()) # get ping status by processing its output
        print("{}".format(ttl), end="")
        if tup[0]:
            print("\t{}".format(tup[1]))
            print("\nPacket reached its destination with {} hops".format(ttl))
            return True
        else:
            print("\t{}".format(tup[1]))
    return False
