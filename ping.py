import platform
import subprocess
import os

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    FNULL = open(os.devnull, 'w')

    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=FNULL,stderr=subprocess.STDOUT) == 0



#for i in range(1,100):
#    address = '127.0.0.' + str(i)
#
#    if not ping(address):
#        print(address + ' did not response.')
#    else:
#        print("ICMP packet recieved from " + address)
