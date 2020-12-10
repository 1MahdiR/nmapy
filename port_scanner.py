import socket
from datetime import datetime

def port_scan(host, port_range=(1,65535), timeout=1):

    target = socket.gethostbyname(host)
    print("Scanning ({}) ports:".format(target))

    for port in range(*port_range):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)

        print("Checking port {}".format(port))
        result = s.connect_ex((target,port))
        if result == 0:
            print("Port {} of ({}) is open".format(port, target))
        s.close()
