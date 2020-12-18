import socket
from datetime import datetime

def port_scan(host_ip, port_range=(1,65535), timeout=1):

    # setting the timeout value for connection
    socket.setdefaulttimeout(timeout)

    open_ports = []
    for port in range(*port_range):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Checking port {}".format(port))
        result = s.connect_ex((host_ip,port))
        if result == 0:
            print("Port {} of ({}) is open".format(port, host_ip))
            open_ports.append(port)
        s.close()
    return open_ports
