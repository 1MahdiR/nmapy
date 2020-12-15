import platform
import subprocess
import os

def ping(host_ip, timeout):

    def f():
        FNULL = open(os.devnull, 'w')

        count_param = '-n' if platform.system().lower()=='windows' else '-c'
        timeout_param = '-w' if platform.system().lower()=='windows' else '-W'

        command = ['ping', count_param, '1', timeout_param, str(timeout), host_ip]

        return subprocess.call(command, stdout=FNULL,stderr=subprocess.STDOUT) == 0

    if f():
        return (True, "ICMP packet recieved from ({})".format(host_ip))
    #else
    return (False, "ICMP packet failed.")

#for i in range(1,100):
#    address = '127.0.0.' + str(i)
#
#    if not ping(address):
#        print(address + ' did not response.')
#    else:
#        print("ICMP packet recieved from " + address)
