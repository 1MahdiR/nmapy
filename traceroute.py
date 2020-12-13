import platform
import subprocess
import socket
import re
import os


# ping argument must be an ip address
def parse_ping_output(output):

    ip_pattern = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"

    is_windows = False
    if platform.system().lower()=='windows':
        is_windows = True

    ls = re.findall(ip_pattern, output)
    print(ls)
    print(output)
    if not is_windows:
        if len(ls) < 3:
            raise Exception("Bad output to process")

        ls = ls[1:-1]

        if len(ls) < 2:
            return (False, '*')

        if re.search('Time to live exceeded', output):
            return (False, ls[1])

        if ls[0] == ls[1]:
            return (True, ls[1])

    else:
        if len(ls) < 2:
            raise Exception("Bad output to process")

        ls = ls[:-1]

        if len(ls) < 2:
            return (False, '*')

        if re.search('TTL expired in transit', output):
            return (False, ls[1])

        if ls[0] == ls[1]:
            return (True, ls[1])

    raise Exception("Unexpected error")

def traceroute(host, hops=30, size=60, timeout=5):

    try:
        host_ip = socket.gethostbyname(host)
    except:
        print("Unable to find {}. Ping failed.".format(host))
        return False

    print("Traceroute to {} ({})\n maximum hops: {}\n {} byte packets\n".format(host, host_ip, hops, size))

    def f(host, ttl):
        FNULL = open(os.devnull, 'w')

        count_param = '-n' if platform.system().lower()=='windows' else '-c'
        ttl_param = '-i' if platform.system().lower()=='windows' else '-t'
        size_param = '-l' if platform.system().lower()=='windows' else '-s'
        timeout_param = '-w' if platform.system().lower()=='windows' else '-W'

        command = ['ping', count_param, '1', ttl_param, str(ttl), size_param, str(size), timeout_param, str(timeout), host]

        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for ttl in range(1, hops+1):
        output = f(host_ip, ttl)
        tup = parse_ping_output(output.stdout.read().decode())
        print("{}".format(ttl), end="")
        if tup[0]:
            print("\t{}".format(tup[1]))
            print("\nPacket reached its destination with {} hops".format(ttl))
            return True
        else:
            print("\t{}".format(tup[1]))
    return False
