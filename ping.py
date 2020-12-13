import platform
import subprocess
import socket
import os

def ping(host):

    try:
        host = socket.gethostbyname(host)
    except:
        print("Unable to find {}. Ping failed.".format(host))
        return False

    print("PING to ({})\nSending ICMP packets...".format(host))

    def f():
        FNULL = open(os.devnull, 'w')

        param = '-n' if platform.system().lower()=='windows' else '-c'

        command = ['ping', param, '1', host]

        return subprocess.call(command, stdout=FNULL,stderr=subprocess.STDOUT) == 0

    if f():
        print("ICMP packet recieved from ({})".format(host))
        return True
    #else
    print("ICMP packet failed.")
    return False

#for i in range(1,100):
#    address = '127.0.0.' + str(i)
#
#    if not ping(address):
#        print(address + ' did not response.')
#    else:
#        print("ICMP packet recieved from " + address)
